# PaymentComplete

## 基本信息

- **事件显示名**: 支付完成
- **事件英文名**: `PaymentComplete`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 | JavaScript | 6.14新增开始有数据<br/><br/>订单支付成功页面展示时上报 (ThankYou页) |  | Checkout 升级<br/>这个用回原来的，不做处理<br/>数据结构用回原来的 只是无法统计“支付类型”跟“支付方式名” |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  |  |
| `discount` | 折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `shipping` | 运费金额 | NUMBER |  | JavaScript |  |  |  |
| `payment_type` | 支付类型 | NUMBER | 直接支付/快捷支付<br/>1=quick_pay<br/>2=direct_pay | JavaScript |  |  |  |
| `payment_name` | 支付方式名 | STRING | Shop pay<br/>Credit Card<br/>PayPal<br/>Afterpay<br/>Klarna<br/>Apple Pay<br/>Google Pay | JavaScript |  |  |  |
| `order` | 订单编号（去重） | STRING | 支付成功订单号 | JavaScript |  |  |  |
| `total` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
| `order_total` | 订单总金额 | NUMBER |  | JavaScript |  |  |  |
| `coupon_discount` | 优惠券折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `giftcard_discount` | GiftCard折扣金额 | NUMBER |  | JavaScript |  |  |  |
