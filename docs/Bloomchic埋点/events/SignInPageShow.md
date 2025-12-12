# SignInPageShow

## 基本信息

- **事件显示名**: 登录页展示
- **事件英文名**: `SignInPageShow`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_page` | 来源页面 | STRING | *必填<br/>个人页、checkout页、支付结果页、购物车，个人设置、通知设置 |  | 页面来源&模块名称枚举：<br/>WEB端<br/>- 个人页-会员中心<br/>-个人页-My Profile<br/>-个人页-My Orders<br/>-个人页-Track Shipping<br/>-个人页-My Reviews<br/>-个人页-My Coupons<br/>-个人页-My Wishlist<br/>-个人页-My Size<br/>-个人页-My Address<br/>-购物车-点击收藏<br/>- checkout页<br/>-支付结果-弹窗<br/>-商详页<br/><br/>APP端<br/>- 个人页-会员中心<br/>-个人页-My Profile<br/>-个人页-My Orders<br/>-个人页-Track Shipping<br/>-个人页-My Reviews<br/>-个人页-My Coupons<br/>-个人页-My Wishlist<br/>-个人页-My Size<br/>-个人页-My Address<br/>-购物车-顶部横幅<br/>-购物车-优惠券模块<br/>-购物车-点击收藏<br/>-设置<br/>-通知设置-Email<br/>-通知设置-SMS<br/>-推送设置<br/>-商详页 |  |  |
| `from_module` | 页面来源模块 | STRING |  |  |  |  |  |
