# ProductRefundSuccess

## 基本信息

- **事件显示名**: 退款成功（SKU维度）
- **事件英文名**: `ProductRefundSuccess`
- **所属模块**: 6.【退货退款】埋点
- **应埋点平台**: 服务端

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING |  | 调用shopify退款接口并且返回退款成功时触发 |  |  |  |
| `product_sku` | 商品SKU | STRING |  |  |  |  |  |
| `product_id` | Shopify Product ID | STRING |  |  |  |  |  |
| `order_time` | 下单时间 |  | 订单创建的时间 |  |  |  |  |
| `order` | 订单编号（去重）短码 | STRING | 订单短码 |  |  |  |  |
| `return_number` | 关联的售后单号 | STRING | 如果有就关了，没有就空 |  |  |  |  |
| `refund_type` | 退款类型 | STRING | 未发货仅退款——商品未发货退款<br/>发货仅退款——关联了发货的商品，但是只退款不退货<br/>退货退款——关联了商品且商品退回仓库后退款<br/>仅退款——没有关联商品，纯退款 |  |  |  |  |
| `refund_price` | 退款金额 | NUMBER | 实际退款金额 |  |  |  |  |
