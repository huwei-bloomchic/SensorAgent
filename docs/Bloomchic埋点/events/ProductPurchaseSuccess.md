# ProductPurchaseSuccess

## 基本信息

- **事件显示名**: 支付成功详情（后端）<br/>按单个商品上报，一次购买多个商品就上报多条
- **事件英文名**: `ProductPurchaseSuccess`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: 

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_list_detail` | [{product_id1,spu1,item_price1,item_quantity1,},{}] | STRING | 一次购买多件不同商品，需要知道不同商品id的购买数量和具体金额 |  |  |  |  |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 |  |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前商品小计金数，税前金额 *数量 |  |  |  |  |
| `discount` | 折扣金额 | NUMBER | 当前SKU商品的折扣 |  |  |  |  |
| `shipping` | 运费金额 | NUMBER |  |  |  |  |  |
| `total` | 总计金额 | NUMBER | 当前商品小计+当前商品的税费-discount |  |  |  |  |
| `tax` | 税 | NUMBER | 当前商品的税费 |  |  |  |  |
| `payment_type` | 支付类型 | NUMBER | 直接支付/快捷支付<br/>1=quick_pay<br/>2=direct_pay |  |  |  |  |
| `payment` | The amount left to be paid. This is equal to the cost of the line items, taxes, and shipping, minus discounts and gift cards. | NUMBER |  |  |  |  |  |
| `order_time` | 下单时间 |  |  |  |  |  |  |
| `payment_name` | 支付方式名 | STRING | Shop pay<br/>Credit Card<br/>PayPal<br/>Afterpay<br/>Klarna<br/>Apple Pay<br/>Google Pay |  |  |  |  |
| `order` | 订单编号（去重） | STRING | 支付成功订单号 |  |  |  |  |
| `distinct_id, $os,$device_id,$app_id, web_platform_type` | 平台类型 | STRING | PC_Web、Mobile_Web、Android、iOS |  |  |  |  |
| `checkout_id` | 结算id | STRING | 结算id |  |  |  |  |
| `product_id` | 单个商品Shopify Product ID |  |  |  |  |  |  |
| `product_spu` | 单个商品spu code |  |  |  |  |  |  |
| `product_sku` | 单个商品sku code |  |  |  |  |  |  |
| `web_original_price` |  |  | SKU原价 |  |  |  |  |
| `web_current_price` |  |  | SKU现价 |  |  |  |  |
| `product_price` | 单个sku商品价格 |  | sku的税前价格，商品售价-折扣金额/数量 |  |  |  |  |
| `product_quantity` | 单个sku商品数量 |  | 买同一个sku的件数，不是订单总的件数 |  |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 新增字段，类型<br/>- 非清仓：no_clearance<br/>- 清仓:clearance |  |  |  |  |
| `return_type` | 退货类型 | STRING | 退货政策：<br/>-可退：return<br/>-不可退：no_return |  |  |  |  |
| `is_quickship` | SKU是否quickship仓发货 | BOOLEAN |  |  |  |  |  |
| `is_fullquickship` | 是否整单quickship仓发货 | BOOLEAN |  |  |  |  |  |
