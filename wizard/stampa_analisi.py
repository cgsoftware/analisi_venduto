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
    _columns = {'analisi_id': fields.many2one('analisi.venduto', 'ID_Analisi'),
                'valore1': fields.float('Totale1', digits=(25,2)),
                'valore2': fields.float('Totale2', digits=(25,2)),
                'valore3': fields.float('Totale3', digits=(25,2)),
                'range1': fields.char('Range1', size=20),
                'range2': fields.char('Range2', size=20),
                'range3': fields.char('Range3', size=20),
                'partner':fields.char('Cliente', size=20),
                'agente':fields.char('Agente', size=20),
                
                }
    

    def carica_doc(self, cr,uid,parametri,context):
        ok = self._pulisci(cr, uid, context)
        periodi_obj = self.pool.get('account.period')
        analisi_obj = self.pool.get('analisi.venduto')
        agente_obj = self.pool.get('sale.agent')
        partner_obj = self.pool.get('res.partner')
        v = {}
        #import pdb;pdb.set_trace()
        if parametri.periodo1 and parametri.partner:
            filtro = [('name', '=', parametri.partner.id), ('periodo_id','=',parametri.periodo1.id)]
        elif parametri.periodo1 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro =[('periodo_id','=',parametri.periodo1.id), ('name','in',partner_ids)]
        else:
            filtro = [('periodo_id','=',parametri.periodo1.id)]
                
        idriga1 = analisi_obj.search(cr, uid, filtro)
        if parametri.periodo2 and parametri.partner:
            filtro2 = [('name', '=', parametri.partner.id), ('periodo_id','=',parametri.periodo2.id)]
        elif parametri.periodo2 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro2 =[('periodo_id','=',parametri.periodo2.id), ('name','in',partner_ids)]
        else:
            filtro2 = [('periodo_id','=',parametri.periodo2.id)]
                
        idriga2 = analisi_obj.search(cr, uid, filtro2)
        if parametri.periodo3 and parametri.partner:
            filtro3 = [('name', '=', parametri.partner.id), ('periodo_id','=',parametri.periodo3.id)]
        elif parametri.periodo3 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro3 =[('periodo_id','=',parametri.periodo3.id), ('name','in',partner_ids)]
        else:
            filtro3 = [('periodo_id','=',parametri.periodo2.id)]
                
        idriga3 = analisi_obj.search(cr, uid, filtro3)
        if idriga1:
            
            for riga in analisi_obj.browse(cr, uid,idriga1):
        #        riga = analisi_obj.browse(cr, uid,idriga1[0])
                rigawr={#'anlisi_id':riga.id,
                         'range1':riga.periodo_id.name,
                         'valore1':riga.totale,
                         'partner':riga.name.name,
                         'agente':riga.name.agent_id.name,
                         }
                ok = self.create(cr,uid,rigawr)
        if idriga2:
            for riga2 in analisi_obj.browse(cr, uid, idriga2):
                cerca2 = [('partner','=',riga2.name.name)]
                idtemp2 = self.search(cr, uid, cerca2)
                if idtemp2:
                    riga_temp = self.browse(cr,uid,idtemp2)[0]
                    rigawr={#'anlisi_id':riga2.id,
                            'range2':riga2.periodo_id.name,
                             'valore2':riga2.totale,
                             }
                    ok = self.write(cr,uid,idtemp2,rigawr)
        if idriga3:
            for riga3 in analisi_obj.browse(cr, uid, idriga3):
                cerca3 = [('partner','=',riga3.name.name)]
                idtemp3 = self.search(cr, uid, cerca3)
                if idtemp3:
                    riga_temp3 = self.browse(cr,uid,idtemp3)[0]
                    rigawr={'range3':riga3.periodo_id.name,
                            'valore3':riga3.totale,
                            }
                    ok = self.write(cr,uid,idtemp3,rigawr)
                #import pdb;pdb.set_trace()             
                #ok = self.create(cr,uid,rigawr)
                             
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
            lista_id = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
        lista_id = tuple(lista_id)
        if parametri.periodo1_1 and parametri.partner:
            filtro = [('name', '=', parametri.partner.id), ('periodo_id','in',lista_id)]
        elif parametri.periodo1_1 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro =[('periodo_id','in',lista_id), ('name','in',partner_ids)]
        else:
            filtro = [('periodo_id','in',lista_id)]
        #import pdb;pdb.set_trace()        
        idriga1 = analisi_obj.search(cr, uid, filtro)
       
        
        if parametri.periodo2_2:
            conteggio = parametri.periodo2.id
            fine = parametri.periodo2_2.id
            lista_id = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
        if parametri.periodo2_2 and parametri.partner:
            filtro2 = [('name', '=', parametri.partner.id), ('periodo_id','in',lista_id)]
        elif parametri.periodo2 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro2 =[('periodo_id','in',lista_id), ('name','in',partner_ids)]
        else:
            filtro2 = [('periodo_id','in',lista_id)]
                
        idriga2 = analisi_obj.search(cr, uid, filtro2)
        
         #TODO MODIFICARE ANCHE PERIODO 3
        if parametri.periodo3_3:
            conteggio = parametri.periodo3.id
            fine = parametri.periodo3_3.id
            lista_id = self.indici_periodi(cr, uid, conteggio, fine, periodi_obj, context)
            
        if parametri.periodo3 and parametri.partner:
            filtro3 = [('name', '=', parametri.partner.id), ('periodo_id','in',lista_id)]
        elif parametri.periodo3 and parametri.agente:
            filtro_ag =[('agent_id','=',parametri.agente.id)]
            partner_ids = partner_obj.search(cr, uid, filtro_ag)
            
            filtro3 =[('periodo_id','in',lista_id), ('name','in',partner_ids)]
        else:
            filtro3 = [('periodo_id','in',lista_id)]
                
        idriga3 = analisi_obj.search(cr, uid, filtro3)
        if idriga1:
            for riga in analisi_obj.browse(cr, uid,idriga1):
                #controllo per prima se non ho già una riga con lo stesso partner
                cerca =  [('partner','=',riga.name.name)]
                idtemp = self.search(cr, uid, cerca)
                if idtemp:
                    temp=self.browse(cr, uid, idtemp)[0]
                    rigawr={#'anlisi_id':riga.id,
                            #'range1':temp.range1.,
                            'valore1':temp.valore1+riga.totale,
                            }
                    ok = self.write(cr,uid,idtemp,rigawr)
                else:
                    rigawr={#'anlisi_id':riga.id,
                         #'range1':riga.periodo_id.name,
                         'valore1':riga.totale,
                         'partner':riga.name.name,
                         'agente':riga.name.agent_id.name,
                         }
                    ok = self.create(cr,uid,rigawr)
        if idriga2:
            for riga2 in analisi_obj.browse(cr, uid, idriga2):
                cerca2 = [('partner','=',riga2.name.name)]
                idtemp2 = self.search(cr, uid, cerca2)
                if idtemp2:
                    riga_temp = self.browse(cr,uid,idtemp2)[0]
                    rigawr={#'anlisi_id':riga2.id,
                            #'range2':riga2.periodo_id.name,
                             'valore2':riga_temp.valore2 + riga2.totale,
                             }
                    ok = self.write(cr,uid,idtemp2,rigawr)
        if idriga3:
            for riga3 in analisi_obj.browse(cr, uid, idriga3):
                cerca3 = [('partner','=',riga3.name.name)]
                idtemp3 = self.search(cr, uid, cerca3)
                if idtemp3:
                    riga_temp3 = self.browse(cr,uid,idtemp3)[0]
                    rigawr={#'range3':riga3.periodo_id.name,
                            'valore3':riga_temp3.valore3 + riga3.totale,
                            }
                    ok = self.write(cr,uid,idtemp3,rigawr)
                #import pdb;pdb.set_trace()             
                #ok = self.create(cr,uid,rigawr)
                             
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
        return self._print_report(cr, uid, ids, data, context=context)
    
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
        
        return self._print_report(cr, uid, ids, data, context=context)
    
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