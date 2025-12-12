# ProductReturnSuccess

## 基本信息

- **事件显示名**: 退货成功（SKU维度）
- **事件英文名**: `ProductReturnSuccess`
- **所属模块**: 6.【退货退款】埋点
- **应埋点平台**: 服务端

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING |  | 调用shopify退款接口时触发 |  |  |  |
| `product_sku` | 商品SKU | STRING |  |  |  |  |  |
| `product_id` | Shopify Product ID | STRING | 商品ID |  |  |  |  |
| `order_time` | 下单时间 |  | 订单创建的时间 |  |  |  |  |
| `order` | 订单编号（去重）短码 | STRING | 订单短码 |  |  |  |  |
| `return_number` | 关联的售后单号 | STRING | 中台售后单编码 |  |  |  |  |
| `return_type` | 退款类型 | STRING | 仅退款、退货退款 |  |  |  |  |
| `refund_price` | 退款金额 | NUMBER | 申请的金额 |  |  |  |  |
| `shipping_price` | 退货运费金额 | NUMBER | 扣减的退货运费 |  |  |  |  |
| `return_reason` | 退货原因 | STRING | 一级二级退货原因文本内容 |  |  |  |  |
