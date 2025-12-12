# CheckOutClick

## 基本信息

- **事件显示名**: 点击Check Out按钮
- **事件英文名**: `CheckOutClick`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_list_detail` | [{product_id1:spu1,item_price1,item_quantity1,},{}] | STRING | 一次购买多件不同商品，需要知道不同商品id的购买数量和具体金额 |  |  |  |  |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript | 购物车中点击CheckOut按钮时上报 |  |  |
| `discount_code` | Copy后的优惠券 | STRING | App2.13新增 |  |  |  |  |
| `cart_type` | 购物车类型 | STRING | 侧边栏展开购物车、完整页面购物车(/Cart) | JavaScript |  |  |  |
| `product_quantity` | 商品数量 | NUMBER | 商品总数(结算按钮上的数字) | JavaScript |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... | JavaScript |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `cart_token` | 购物车的Token | STRING | 在新的CheckOut SDK下需要上报该数据 |  |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 | JavaScript |  |  |  |
| `is_best_coupon` | 优惠券是否为最优券：是/否 | INT | 1表示1，0表示否 | APP3.6新增 |  |  |  |
| `coupon_source` | 优惠券来源 | STRING | 0=平台阶梯券&用户券包券；1=用户输入 | APP3.6新增 |  |  |  |
| `coupon_type` | 优惠券类型 | INT | 1：百分比优惠，2：金额优惠，3：免运费 4: 折扣券但是限制个数<br/>和后端返回的int一致 | APP3.6新增 |  |  |  |
| `discount_code` | 优惠券code | STRING | App2.13新增 |  |  |  |  |
| `web_discount_price` | 优惠券优惠金额 | NUMBER | 应用的券扣减金额 | APP3.6新增 |  |  |  |
| `is_fullquickship` | 是否整单quickship仓发货 | BOOLEAN |  |  |  |  |  |
| `quickship_skus` | quickship仓发货的SKU编码 | STRING |  |  |  |  |  |
| `giftcard_code` | giftcard_code | STRING | 选择的giftcard_code，如code1;code2 | APP3.6新增 |  |  |  |
| `giftcard_price` | giftcard金额 | NUMBER | 选中的giftcard的余额合计；比如49.99 | APP3.6新增 |  |  |  |
