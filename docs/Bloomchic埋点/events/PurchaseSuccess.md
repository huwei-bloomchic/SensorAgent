# PurchaseSuccess

## 基本信息

- **事件显示名**: 支付成功（支付（后端）（Android 2.8）
- **事件英文名**: `PurchaseSuccess`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: 

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_list_detail` | [{product_id1,spu1,item_price1,item_quantity1,},{}] | STRING | 一次购买多件不同商品，需要知道不同商品id的购买数量和具体金额 |  |  |  |  |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 |  |  | Android2.8 & iOS2.6 |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 |  |  |  |  |
| `discount` | 折扣金额 | NUMBER |  |  |  |  |  |
| `shipping` | 运费金额 | NUMBER |  |  |  |  |  |
| `total` | 总计金额 | NUMBER |  |  |  |  |  |
| `payment_type` | 支付类型 | NUMBER | 直接支付/快捷支付<br/>1=quick_pay<br/>2=direct_pay |  |  |  |  |
| `payment` | The amount left to be paid. This is equal to the cost of the line items, taxes, and shipping, minus discounts and gift cards. | NUMBER |  |  |  |  |  |
| `order_time` | 下单时间 |  |  |  |  |  |  |
| `payment_name` | 支付方式名 | STRING | Shop pay<br/>Credit Card<br/>PayPal<br/>Afterpay<br/>Klarna<br/>Apple Pay<br/>Google Pay |  |  |  |  |
| `order` | 订单编号（去重） | STRING | 支付成功订单号 |  |  |  |  |
| `order_id` | 订单长编号 |  |  |  |  |  |  |
| `order_app_id` |  |  |  |  |  |  |  |
| `tax` |  | NUMBER |  |  |  |  |  |
| `credit_card_wallet` |  |  |  |  |  |  |  |
| `is_fullquickship` | 是否整单quickship仓发货 | BOOLEAN |  |  |  |  |  |
| `quickship_skus` | quickship仓发货的SKU编码 | STRING |  |  |  |  |  |
| `cart_token` |  | STRING | Shopify 订单cart token |  |  |  |  |
| `distinct_id, $os,$device_id,$app_id, web_platform_type` | 平台类型 | STRING | PC_Web、Mobile_Web、Android、iOS |  |  |  |  |
| `checkout_id` | 结算id，checkout token | STRING | Shopify 订单的checkout token |  |  |  |  |
