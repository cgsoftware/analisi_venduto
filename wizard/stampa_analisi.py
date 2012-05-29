# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _
from datetime import datetime, timedelta
import base64
from tempfile import TemporaryFile
import math

import tools
import ir
import base64


#from tools.translate import _
import csv
import sys
import os
import re

class tempstatistiche_analisi(osv.osv):
    
    def _pulisci(self,cr,uid,context):
        ids = self.search(cr,uid,[])
        ok = self.unlink(cr,uid,ids,context)
        return True
    
    _name = 'tempstatistiche.analisi'
    _description = 'temporaneo per la stampa delle analisi del venduto'
    _columns = {
                'valore1': fields.float('Totale1', digits=(25,2)),
                'valore2': fields.float('Totale2', digits=(25,2)),
                'valore3': fields.float('Totale3', digits=(25,2)),
                'partner_id':fields.many2one('res.partner', 'Cliente'),
                'partner':fields.char('Cliente', size=70),
                'agente':fields.char('Agente', size=70),
                
                }
    _order = 'agente, valore1, partner'
    

    def carica_doc(self, cr,uid,parametri,context):
        ok = self._pulisci(cr, uid, context)
        periodi_obj = self.pool.get('account.period')
        analisi_obj = self.pool.get('analisi.venduto')
        agente_obj = self.pool.get('sale.agent')
        partner_obj = self.pool.get('res.partner')
        
        if parametri.partner:
            partner_ids = parametri.partner.id
        elif parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
        else:
            partner_ids= partner_obj.search(cr, uid, [])
        if partner_ids:
            for partner in partner_obj.browse(cr, uid, partner_ids):
              if partner.venduto:
                
                    cerca =[('periodo_id','=', parametri.periodo1.id), ('name', '=', partner.id)]
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    #import pdb;pdb.set_trace()
                    if riga_analisi:
                        riga_valore = analisi_obj.browse(cr, uid, riga_analisi[0])
                        rigawr={#'anlisi_id':riga.id,
                            
                                'valore1':riga_valore.totale,
                                'partner_id':partner.id,
                                'partner':partner.name,
                                'agente':partner.agent_id.name,
                                }
                        ok = self.create(cr,uid,rigawr)
                    cerca =[('periodo_id','=', parametri.periodo2.id) , ('name', '=', partner.id)]
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    if riga_analisi:
                        riga_valore = 0
                        riga_valore = analisi_obj.browse(cr, uid, riga_analisi[0])
                        trova = [('partner_id','=',partner.id)]
                        id_temp = self.search(cr, uid, trova)
                        if id_temp:
                            rigawr={'valore2':riga_valore.totale,}
                            ok = self.write(cr,uid,id_temp,rigawr)
                            id_temp = 0
                        else:
                            rigawr={'valore1':0,
                                    'partner_id':partner.id,
                                    'partner':partner.name,
                                    'agente':partner.agent_id.name,
                                    'valore2':riga_valore.totale,
                                    }
                            ok = self.create(cr,uid,rigawr)
                    cerca =[('periodo_id','=', parametri.periodo3.id), ('name', '=', partner.id)] 
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    if riga_analisi:
                        riga_valore = 0
                        riga_valore = analisi_obj.browse(cr, uid, riga_analisi[0])
                        trova = [('partner_id','=',partner.id)]
                        id_temp = self.search(cr, uid, trova)
                        if id_temp:
                            rigawr={'valore3':riga_valore.totale,}
                            ok = self.write(cr,uid,id_temp,rigawr)
                            id_temp = 0
                        else:
                            rigawr={'valore1':0,
                                    'valore2':0,
                                    'partner_id':partner.id,
                                    'partner':partner.name,
                                    'agente':partner.agent_id.name,
                                    'valore3':riga_valore.totale,
                                    }
                            ok = self.create(cr,uid,rigawr)
                             
        return True
    def indici_periodi(self, cr, uid, conteggio, fine, periodi_obj, context):
        result=[]
        sommaid = conteggio
        result.append(conteggio)
        if conteggio == fine:
            continua = False
        else:
            continua = True
        
        #import pdb;pdb.set_trace()
        while continua:
            sommaid += 1
            nuovo_id = periodi_obj.browse(cr, uid, sommaid)
            result.append(nuovo_id.id)
            if sommaid == fine:
                continua = False
            
                
        
        return result
    
    def carica_doc_somma(self, cr,uid,parametri,context):
        ok = self._pulisci(cr, uid, context)
        periodi_obj = self.pool.get('account.period')
        analisi_obj = self.pool.get('analisi.venduto')
        agente_obj = self.pool.get('sale.agent')
        partner_obj = self.pool.get('res.partner')
        v = {}
        #import pdb;pdb.set_trace() idsTipoDoc = tuple(idsTipoDoc)
             
        
        
        
        if parametri.periodo1_1:
            conteggio = parametri.periodo1.id
            fine = parametri.periodo1_1.id
            lista_id1 = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
            
        if parametri.periodo2_2:
            conteggio = parametri.periodo2.id
            fine = parametri.periodo2_2.id
            lista_id2 = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
        if parametri.periodo3_3:
            conteggio = parametri.periodo3.id
            fine = parametri.periodo3_3.id
            lista_id3 = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
        
        if parametri.partner:
            partner_ids = parametri.partner.id
        elif parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
        else:
            partner_ids= partner_obj.search(cr, uid, [])
        if partner_ids:
            for partner in partner_obj.browse(cr, uid, partner_ids):
                if partner.venduto:
                    cerca =[('periodo_id','in', lista_id1), ('name', '=', partner.id)]
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    if riga_analisi:
                        for riga in analisi_obj.browse(cr, uid, riga_analisi):
                            trova = [('partner_id','=',partner.id)]
                            id_temp = self.search(cr, uid, trova)
                            if id_temp:
                                temp=self.browse(cr, uid, id_temp)[0]
                                rigawr={'valore1':temp.valore1+riga.totale,
                                        }
                                ok = self.write(cr,uid,id_temp,rigawr)
                            else:
                                rigawr={
                                    'partner_id':partner.id,
                                    'partner':partner.name,
                                    'agente':partner.agent_id.name,
                                    'valore1':riga.totale,
                                    }
                                ok = self.create(cr,uid,rigawr)
                    cerca =[('periodo_id','in', lista_id2), ('name', '=', partner.id)]
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    if riga_analisi:
                        for riga in analisi_obj.browse(cr, uid, riga_analisi):
                            trova = [('partner_id','=',partner.id)]
                            id_temp = self.search(cr, uid, trova)
                            #import pdb;pdb.set_trace()
                            if id_temp:
                                temp=self.browse(cr, uid, id_temp)[0]
                                rigawr = {'valore2':temp.valore2+riga.totale,}
                                ok = self.write(cr,uid,id_temp,rigawr)
                            else:
                                rigawr={
                                        'partner_id':partner.id,
                                        'partner':partner.name,
                                        'agente':partner.agent_id.name,
                                        'valore1':0,
                                        'valore2':riga.totale,
                                    }
                                ok = self.create(cr,uid,rigawr)
                    cerca =[('periodo_id','in', lista_id3), ('name', '=', partner.id)]
                    riga_analisi = analisi_obj.search(cr, uid, cerca)
                    if riga_analisi:
                        for riga in analisi_obj.browse(cr, uid, riga_analisi):
                            trova = [('partner_id','=',partner.id)]
                            id_temp = self.search(cr, uid, trova)
                            if id_temp:
                                temp=self.browse(cr, uid, id_temp)[0]
                                rigawr = {'valore3':temp.valore3+riga.totale,}
                                ok = self.write(cr,uid,id_temp,rigawr)
                            else:
                                rigawr={
                                        'partner_id':partner.id,
                                        'partner':partner.name,
                                        'agente':partner.agent_id.name,
                                        'valore1':0,
                                        'valore2':0,
                                        'valore3':riga.totale,
                                    }
                                ok = self.create(cr,uid,rigawr)
        return True
        
            
            
                
        
        

tempstatistiche_analisi()

class stampa_analisi_venduto (osv.osv_memory):
    _name = 'stampa.analisi.venduto'
    _description = 'parametri di stampa jasper per le analisi del venduto'
    _columns = {'periodo1': fields.many2one('account.period', 'Periodo anno n', required=True),
                'periodo1_1':fields.many2one('account.period', 'A Periodo anno n'),
                'periodo2': fields.many2one('account.period', 'Periodo anno n-1', required=True),
                'periodo2_2':fields.many2one('account.period', 'A Periodo anno n-1'),
                'periodo3': fields.many2one('account.period', 'Periodo anno n-2', required=True),
                'periodo3_3':fields.many2one('account.period', 'A Periodo anno n-2'),
                'partner':fields.many2one('res.partner', 'Cliente'),
                'agente':fields.many2one('sale.agent', 'Agente'),
                'export_csv':fields.boolean('Genera CSV')
                }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
        parametri = self.browse(cr,uid,ids)[0]
        if parametri.periodo1_1:
            periodo1 = parametri.periodo1.name + '-' + parametri.periodo1_1.name
            periodo2 = parametri.periodo2.name + '-' + parametri.periodo2_2.name
            periodo3 = parametri.periodo3.name + '-' + parametri.periodo3_3.name
            result = {'periodo1':periodo1,'periodo2':periodo2,'periodo3':periodo3,
                      'partner':parametri.partner.name,'agente':parametri.agente.name}
        
        else:
            result = {'periodo1':parametri.periodo1.name,'periodo2':parametri.periodo2.name,'periodo3':parametri.periodo3.name,
                      'partner':parametri.partner.name,'agente':parametri.agente.name}
        return result
        
    def _print_report(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['periodo1',  'periodo2','periodo3','partner','agente'])[0]
        #used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['parameters'] = self._build_contexts(cr, uid, ids, data, context=context)
        #import pdb;pdb.set_trace()
        parametri = self.browse(cr,uid,ids)[0]
        if not parametri.agente:
            data['form']['parameters']['agente']=""
        if not parametri.partner:
            data['form']['parameters']['partner']=""
        pool = pooler.get_pool(cr.dbname)
        #fatture = pool.get('fiscaldoc.header')
        active_ids = context and context.get('active_ids', [])
        return {
                            'type': 'ir.actions.report.xml',
                            'report_name':'venduto',
                            'datas': data,
                            }
        
    def check_report(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
            
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['dadata1_1', 'dadata1_2', 'dadata2_1', 'dadata2_2', 'dadata3_1', 'dadata3_2', 'partner', 'agente'])[0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['parameters'] = used_context
        parametri = self.browse(cr,uid,ids)[0]
        if parametri.export_csv:
            return  {
                             'name': 'Export Analisi Vendite',
                             'view_type': 'form',
                             'view_mode': 'form',
                             'res_model': 'crea_csv_analisi_v',
                             'type': 'ir.actions.act_window',
                             'target': 'new',
                             'context': context                            
                             
                             }
        else:
            return self._print_report(cr, uid, ids, data, parametri, context=None)
        return
        
    
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(stampa_ordini, self).view_init(cr, uid, fields_list, context=context)

        return res
    
    def  default_get(self, cr, uid, fields, context=None):
       
        pool = pooler.get_pool(cr.dbname)
        docs = pool.get('fiscaldoc.header')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
             #import pdb;pdb.set_trace()
             for docu in docs.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
        #            DtIni = docu['data_documento']
        #            NrIni = docu['name']
                    danr = docu['id']
                
         #       DtFin = docu['data_documento']
      #          NrFin = docu['name']
                anr = docu['id']  
              
        return {}
    
    def crea_temp(self,cr, uid, ids, data, context=None):
        parametri = self.browse(cr,uid,ids)[0]
        #import pdb;pdb.set_trace()
        
        if parametri.partner and parametri.agente:
            raise osv.except_osv(_('ERRORE !'), _('NON È POSSIBILE SELEZIONARE CONTEMPORANEMATE AGENTE E CLIENTE'))
        else:
            if parametri.periodo1_1:
                ok = self.pool.get('tempstatistiche.analisi').carica_doc_somma(cr,uid,parametri,context)
            else:
                ok = self.pool.get('tempstatistiche.analisi').carica_doc(cr,uid,parametri,context)
        
        return self.check_report(cr, uid, ids, context=None)
    
    def on_change_value(self, cr, uid, ids, periodo1, context):
        
        v = {}
        periodi_obj = self.pool.get('account.period')
        periodo = periodi_obj.browse(cr, uid, periodo1)
        dt = periodo.date_start
        data_1 = datetime.strptime(dt, '%Y-%m-%d')
        anno = data_1.year
        anno = anno - 1
        giorno = data_1.day
        mese = data_1.month
        giornos = str(giorno).zfill(2)
        meses = str(mese).zfill(2)
        annos = str(anno)
        nuova_data = annos + "-" + meses + "-" + giornos
        filtro = [('date_start', '=', nuova_data)]
        nuovo_id = periodi_obj.search(cr, uid, filtro)
        #import pdb;pdb.set_trace()

        if nuovo_id:
            v['periodo2']=nuovo_id[0]
            anno = anno - 1
            annos = str(anno)
            nuova_data = annos + "-" + meses + "-" + giornos
            filtro = [('date_start', '=', nuova_data)]
            secondo_id = periodi_obj.search(cr, uid, filtro)
            if secondo_id:
                
                v['periodo3']=secondo_id[0]
        return {'value': v}
    
    def on_change_value2(self, cr, uid, ids, periodo1_1, context):
        
        v = {}
        periodi_obj = self.pool.get('account.period')
        periodo = periodi_obj.browse(cr, uid, periodo1_1)
        dt = periodo.date_start
        data_1 = datetime.strptime(dt, '%Y-%m-%d')
        anno = data_1.year
        anno = anno - 1
        giorno = data_1.day
        mese = data_1.month
        giornos = str(giorno).zfill(2)
        meses = str(mese).zfill(2)
        annos = str(anno)
        nuova_data = annos + "-" + meses + "-" + giornos
        filtro = [('date_start', '=', nuova_data)]
        nuovo_id = periodi_obj.search(cr, uid, filtro)
        #import pdb;pdb.set_trace()

        if nuovo_id:
            v['periodo2_2']=nuovo_id[0]
            anno = anno - 1
            annos = str(anno)
            nuova_data = annos + "-" + meses + "-" + giornos
            filtro = [('date_start', '=', nuova_data)]
            secondo_id = periodi_obj.search(cr, uid, filtro)
            if secondo_id:
                
                v['periodo3_3']=secondo_id[0]
        return {'value': v}
                    
stampa_analisi_venduto()


class crea_csv_analisi_v(osv.osv_memory):
    _name = "crea_csv_analisi_v"
    _description = "Crea il csv dal temporaneo analisi delle vendite"
    _columns = {
                    'state': fields.selection((('choose', 'choose'), # choose accounts
                                               ('get', 'get'), # get the file
                                   )),
                    #'nomefile':fields.char('Nome del file',size=20,required = True)
                    'data': fields.binary('File', readonly=True),

                    }
    _defaults = {
                 'state': lambda * a: 'choose',
                 }
    
    def generacsvanalisi(self, cr, uid, ids,context=None):
        if ids:
            stampa_obj = self.pool.get('stampa.analisi.venduto')
            parametri = stampa_obj.browse(cr, uid, ids)[0]
            idts = self.pool.get('tempstatistiche.analisi').search(cr,uid,[])
            if idts:
                #import pdb;pdb.set_trace()
                File = """"""""
                Record =""
                Record += '"'+"Agente"+'";'
                Record += '"'+"Cliente"+'";'
                Record += '"'+ parametri.periodo1.name + '-' + parametri.periodo1_1.name +'";'
                Record += '"'+ parametri.periodo2.name + '-' + parametri.periodo2_2.name +'";'
                Record += '"'+ parametri.periodo3.name + '-' + parametri.periodo3_3.name +'";'
                Record += "\r\n"
                for riga in self.pool.get('tempstatistiche.analisi').browse(cr,uid,idts, context):
                    Record += '"'+ riga.agente +'";'
                    Record += '"'+ riga.partner_id.name +'";'
                    Record += '"'+ str(riga.valore1) + '";' 
                    Record += '"'+ str(riga.valore2) + '";'
                    Record += '"'+ str(riga.valore3) + '";'
                    Record += "\r\n"
                #import pdb;pdb.set_trace()
                File += Record
                out = base64.encodestring(File)   
                           
                return self.write(cr, uid, ids, {'state':'get', 'data':out}, context=context)
            else:
                return {'type': 'ir.actions.act_window_close'}
        

crea_csv_analisi_v()    