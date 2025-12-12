# CheckOutStart

## 基本信息

- **事件显示名**: 结算开始(app端特有)
- **事件英文名**: `CheckOutStart`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `checkout_id` | 结算id | STRING | 结算id |  |  |  |  |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 |  |  |  |  |
| `discount_code` | Copy后的优惠券 | STRING | App2.13新增 |  |  |  |  |
| `cart_type` | 购物车类型 | STRING | 侧边栏展开购物车、完整页面购物车(/Cart) |  |  |  |  |
| `product_quantity` | 商品数量 | NUMBER | 商品总数(结算按钮上的数字) |  |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | SPU1;SPU2;SPU3;.......... |  |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `product_sku_list` | 商品SKU列表 | STRING | SKU1;SKU2;SKU3;.......... |  |  |  |  |
| `cart_token` | 购物车的Token | STRING | 在新的CheckOut SDK下需要上报该数据 |  |  |  |  |
| `subtotal` | 小计金额 | NUMBER | 当前小计金数，比如$49.99 |  |  |  |  |
