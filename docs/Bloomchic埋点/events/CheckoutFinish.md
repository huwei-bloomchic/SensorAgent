# CheckoutFinish

## 基本信息

- **事件显示名**: 支付结果，手机端专属，由于调用H5 进行结算，增加上报用来交叉验证
- **事件英文名**: `CheckoutFinish`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `checkout_id` | 结算id | STRING | 结算id |  |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING |  |  |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING |  |  |  |  |  |
| `subtotal` | 小计金额 | NUMBER |  |  |  |  |  |
| `payment` | 还需要支付的金额，The amount left to be paid. This is equal to the cost of the line items, taxes, and shipping, minus discounts and gift cards. | NUMBER | 还需要支付的金额， |  |  |  |  |
| `shipping` | 运费金额 | NUMBER | app拿不到具体的运费，所以没有上报 |  |  |  |  |
| `total` | 总计金额 | NUMBER |  |  |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `product_quantity` | 商品数量 | NUMBER |  |  |  |  |  |
| `cart_token` | 购物车的Token | STRING | 在新的CheckOut SDK下需要上报该数据 |  |  |  |  |
| `order` | 支付成功：订单名；失败： null | STRING |  |  |  |  |  |
