# PayNowButtonClick

## 基本信息

- **事件显示名**: 点击Pay now
- **事件英文名**: `PayNowButtonClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `shopify_payment_method` | 支付方式 | INT | 1=Credit Card<br/>2=PayPal | JavaScript | 点击Pay now/Complete order按钮时上报 |  | Checkout 升级<br/>如果用户不选择支付方式<br/>direct_payment_name 是没有办法获取的 |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 | JavaScript |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... | JavaScript |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... | JavaScript |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  |  |
| `discount` | 订单折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `shipping` | 运费金额 | NUMBER |  | JavaScript |  |  |  |
| `direct_payment_name` | 直接支付方式 | STRING |  | JavaScript |  |  |  |
| `total` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
| `order_total` | 订单总金额 | NUMBER |  | JavaScript |  |  |  |
| `coupon_discount` | 优惠券折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `giftcard_discount` | GiftCard折扣金额 | NUMBER |  | JavaScript |  |  |  |
