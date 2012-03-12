# -*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math

from tools.translate import _

from osv import fields, osv

class partner(osv.osv):

    _inherit = 'res.partner'
    
    _columns = {                            
                'venduto':fields.one2many('analisi.venduto', 'name', 'partner_id'),

                }
    
    

partner()