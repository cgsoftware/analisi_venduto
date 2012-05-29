import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _

class lancio_manuale(osv.osv_memory):
    _name = 'parcalcolo.analisi.venduto'
    _description = 'paramentri per il calcolo del venduto partner manuale'
    _columns = {'periodo':fields.many2one('account.period', 'Periodo', required=True),
                'partner':fields.many2one('res.partner', 'Cliente'),
                'tutti':fields.boolean('Aggiorno tutti i clienti del periodo?', required=False)}
    
    
    def agg_dati(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        parametri = self.browse(cr,uid,ids)[0]
        periodo = parametri.periodo
        partner = parametri.partner
        partner_obj = self.pool.get('res.partner')
        if parametri.tutti:
            partner=0
            res = self.pool.get('analisi.venduto')._import_analisi_vendite(cr, uid, partner_obj, periodo, partner,context)
        else:
            res = self.pool.get('analisi.venduto')._import_analisi_vendite(cr, uid, partner_obj, periodo, partner,context)

        
        return {'type': 'ir.actions.act_window_close'}
    
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(lancio_manuale, self).view_init(cr, uid, fields_list, context=context)
        
        return res
    
             
    def  default_get(self, cr, uid, fields, context=None):
        #import pdb;pdb.set_trace()
        pool = pooler.get_pool(cr.dbname)
        partner_obj = self.pool.get('res.partner')
        active_ids = context and context.get('active_ids', [])
        Primo = True
        if active_ids:
            for partner in partner_obj.browse(cr, uid, active_ids, context=context):
                if Primo:
                    Primo = False
                    cliente = partner['id']

                
        
        return{'partner':cliente}
    
   
         
lancio_manuale()