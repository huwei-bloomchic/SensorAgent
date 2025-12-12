# CheckoutShippingSelect

## 基本信息

- **事件显示名**: 选择邮寄方式 【Shipping method】
- **事件英文名**: `CheckoutShippingSelect`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `shipping_name` | 选中邮寄名 | STRING |  | JavaScript | 点击触发 |  | Checkout 升级<br/>未登录的情况下能监听的到<br/>或者未保存过地址 |
| `shipping_amount` | 选中邮寄邮费 | STRING |  | JavaScript |  |  |  |
