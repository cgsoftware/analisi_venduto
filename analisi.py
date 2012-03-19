# -*- encoding: utf-8 -*-

import decimal_precision as dp
import time
import base64
from tempfile import TemporaryFile
import math
from osv import fields, osv
import tools
import ir
import pooler
import tools
#from tools.translate import _
import csv
import sys
import os
import re


from datetime import datetime, timedelta

class analisi_vendite (osv.osv):
    _name = 'analisi.venduto'
    _description = 'Tabella di riepilogo del venduto di periodo'
    _columns = {
                'name':fields.many2one('res.partner', 'Cliente', required=True, ondelete='cascade', select=True, readonly=True),
                #'partner_id': fields.many2one('res.partner', 'Partner', ondelete='cascade', help="Inserisci l'eventuale cliente/fornitore"),
                'periodo_id': fields.many2one('account.period', 'Periodo', required=True),
                'totale':fields.float('Totale', digits=(25,2)),
                
                }
    
    
    
    def _import_analisi_vendite(self, cr, uid, partner_obj, periodo, partner,context):
        testa=self.pool.get('fiscaldoc.header')
        filtro1 = [('tipo_documento', 'in', ('FA','FI','FD','NC'))] #AGGIUNGERE NOTE CREDITO E NOTE DEBITO
        idsTipoDoc = self.pool.get('fiscaldoc.causalidoc').search(cr, uid, filtro1)
        idsTipoDoc = tuple(idsTipoDoc)
        #import pdb;pdb.set_trace()
        #filtro_data=[('data_documento','=','2012-01-31' )]
        if partner<>0:
            filtro_data=[('data_documento','<=',periodo.date_stop ),('data_documento','>=', periodo.date_start ),('tipo_doc','in',idsTipoDoc),('partner_id','=', partner.id)]
        else:
            filtro_data=[('data_documento','<=',periodo.date_stop ),('data_documento','>=', periodo.date_start ),('tipo_doc','in',idsTipoDoc)]
        testate_ids = testa.search(cr, uid, filtro_data)
        
        #filtro_clienti=[('customer','=','TRUE')]
        #clienti = self.pool.get('res.partner').search(cr, uid, filtro_clienti)
        
        #for partner in self.pool.get('res.partner').browse(cr, uid, clienti):
        for doc in testa.browse(cr, uid, testate_ids):
            
                cerca = [('name','=',doc.partner_id.id)]
                id_temp = self.search(cr,uid,cerca)
                    #CERCO NELLEn RIGHE GIA' SCRITTE IL CLIENTE APPENA LETTO
                if id_temp:
                        #import pdb;pdb.set_trace()
                        riga_temp = self.browse(cr,uid,id_temp)[0]
                        
                        id_temp2=self.search(cr, uid, [('name','=',doc.partner_id.id),('periodo_id','=', periodo.id)])
                        #CERCO NEL CLIENTE LA CORRISPONDENZA DEL PERIODO
                        if id_temp2:
                            riga_temp2 = self.browse(cr,uid,id_temp2)[0]
                            if doc.tipo_doc.tipo_documento == 'NC':
                                rigawr={'totale':riga_temp2.totale-doc.totale_netto_merce}#totale_netto merce
                            else:
                                rigawr={'totale':riga_temp2.totale+doc.totale_netto_merce}#totale_netto merce
                            ok = self.write(cr,uid,id_temp2,rigawr)
                        else:
                            if doc.tipo_doc.tipo_documento == 'NC':
                                rigawr={#'partner_id':doc.partner_id.id,
                                        'name':doc.partner_id.id,
                                        'periodo_id':periodo.id,
                                        'totale':doc.totale_merce*-1}
                            else:
                                rigawr={#'partner_id':doc.partner_id.id,
                                        'name':doc.partner_id.id,
                                        'periodo_id':periodo.id,
                                        'totale':doc.totale_merce}
                            
                            ok = self.create(cr,uid,rigawr)
                else:
                    if doc.tipo_doc.tipo_documento == 'NC':
                        rigawr={#'partner_id':doc.partner_id.id,
                                'name':doc.partner_id.id,
                                'periodo_id':periodo.id,
                                'totale':doc.totale_merce*-1,}
                    else:
                        rigawr={#'partner_id':doc.partner_id.id,
                                'name':doc.partner_id.id,
                                'periodo_id':periodo.id,
                                'totale':doc.totale_merce,}
                    
                        #
                    ok = self.create(cr,uid,rigawr)
        return            
                       
            
    def run_auto_import_analisi(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        pool = pooler.get_pool(cr.dbname)  
        res = {}
        
        
        testo_log = """Inizio procedura di Aggiornamento/Venduto per clienti """ + time.ctime() + '\n'
        print testo_log
        if use_new_cursor:
            cr = pooler.get_db(use_new_cursor).cursor()
        periodi_obj = self.pool.get('account.period')
        partner_obj = self.pool.get('res.partner')
        #TODO moficicare con anno fiscale in corso
        dt = time.strftime('%Y-%m-%d')
        data_sca = datetime.strptime(dt, '%Y-%m-%d')
        giorno = data_sca.day
        mese = data_sca.month
        anno = data_sca.year
        # controlli per le giuste date del fine mese 
        giornos = str(giorno).zfill(2)
        meses = str(mese).zfill(2)
        annos = str(anno)
        mese_prec = str(mese - 1).zfill(2)
        #import pdb;pdb.set_trace()
        
        if mese_prec in "04-06-09-11":
            data = annos + "-" + mese_prec + "-" + "30"
        else:
            data = annos + "-" + mese_prec + "-" + "31"
        if mese_prec in "02":
            data = annos + "-" + mese_prec + "-" + "28"
        pos = 1
        while pos > 0 :    
            filtro = [('date_stop','=',data)]
            periodo_id = periodi_obj.search(cr, uid, filtro)
            if periodo_id:
                pos = -10
            data = annos + "-" + mese_prec + "-" + "29"
            pos = pos +1
        for periodo in periodi_obj.browse(cr, uid, periodo_id):
            partner = 0
            res = self._import_analisi_vendite(cr, uid, partner_obj, periodo, partner,context)
        testo_log = testo_log + " Operazione Terminata  alle " + time.ctime() + "\n"
        print testo_log
        return True
    
    def run_auto_import_analisi_precedenti(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
      pool = pooler.get_pool(cr.dbname)  
      res = {}
      testo_log = """Inizio procedura di Aggiornamento/Inserimento Analisi anni precedenti """ + time.ctime() + '\n'
      print testo_log
      percorso ='/home/openerp/filecsv' #'/home/andrea/openerp/filecsv'
      partner_obj = self.pool.get('res.partner')
      analisi_obj = self.pool.get('analisi.venduto')
      periodo_obj = self.pool.get('account.period')
      if use_new_cursor:
        cr = pooler.get_db(use_new_cursor).cursor()
      elenco_csv = os.listdir(percorso)
      for filecsv in elenco_csv:
          
          lines = csv.reader(open(percorso + '/' + filecsv, 'rb'), delimiter=",")
          inseriti = 0
          for riga in  lines:
              
              filtro = [('ref', '=', riga[0])  ]
              partner = partner_obj.search(cr,uid,filtro)
              #ho trovato l'id del partner
              #ricostruisco il periodo
              giornos = str(riga[2]).zfill(2)
              data=giornos+'/'+riga[1]
              filtro2 = [('name','=',data)]
              periodo = periodo_obj.search(cr,uid, filtro2)
              #ho trovato l'id della riga del periodo
              #import pdb;pdb.set_trace()
              riga_wr = {'name' : partner[0],
                         'periodo_id': periodo[0],
                         'totale':riga[3].replace(',', '.'),
                     
                        }
              ok = analisi_obj.create(cr, uid, riga_wr)
              inseriti = inseriti + 1
              testo_log = """FINE procedura di Aggiornamento/Inserimento Analisi anni precedenti""" + time.ctime() + '\n'
              print testo_log
              print inseriti      
      return True
  
          
    
 

 
analisi_vendite()

