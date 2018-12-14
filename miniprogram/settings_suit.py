# coding=utf8

# Django suit配置
SUIT_CONFIG = {
    'ADMIN_NAME': '保保回收管理后台',
    'LIST_PER_PAGE': 30,
    'MENU_ORDER': (
        ('sites',),

        (('用户管理', ''),
         (
             ('用户管理','/bg/business_sys/recyclingstaffinfo/'),
         )
         ),
        (('订单管理', ''),
         (
             ('创建流动站订单', '/bg/ordersys/orderinfo/add/'),
             ('订单汇总', '/bg/ordersys/orderinfo/'),
         )
         ),
        (('价格管理', ''),
         (
             ('价格列表', '/bg/business_sys/businessproducttypebind/'),
         )
         ),
        (('客服任务', ''),
         (
             ('一健回收调度', '/bg/ordersys/orderinfo/'),
             ('认证', '/bg/usersys/wechatusercontext/'),
         )
         ),
        (('地图监控', ''),
         (
             ('实时位置监控', ''),
         )
         ),


    )
    # 'MENU_EXCLUDE': ('auth.group', 'auth'),
    # 'MENU': (
    #     'sites',
    #     {'label': 'basic', 'icon': 'icon-cog', 'url': '/admin/basic/companyinfo/1/change/'}
    # )
}
