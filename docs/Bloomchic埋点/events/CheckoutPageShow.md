# CheckoutPageShow
CheckOutPageShow 也同时上报，不影响线上的数据

## 基本信息

- **事件显示名**: 结算页展示
- **事件英文名**: `CheckoutPageShow
CheckOutPageShow 也同时上报，不影响线上的数据`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_quantity` | 商品数量 | NUMBER | 商品总数 | JavaScript | 结算页展示时上报<br/>要等页面信息初始完才上报 |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... | JavaScript |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... | JavaScript |  |  | code有一些用的是shopify productid，需要转成spu和sku |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  | code有一些用的是shopify productid，需要转成spu和sku |
| `discount` | 订单折扣金额 | NUMBER |  | JavaScript |  |  | Checkout 升级 |
| `shipping` | 运费金额 | NUMBER |  | JavaScript |  |  |  |
| `total` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
| `order_total` | 订单总金额 | NUMBER |  | JavaScript |  |  |  |
| `is_fullquickship` | 是否整单quickship仓发货 | BOOLEAN |  |  |  |  |  |
| `quickship_skus` | quickship仓发货的SKU编码 | STRING |  |  |  |  |  |
| `coupon_discount` | 优惠券折扣金额 | NUMBER |  | JavaScript |  |  |  |
| `giftcard_discount` | GiftCard折扣金额 | NUMBER |  | JavaScript |  |  |  |
