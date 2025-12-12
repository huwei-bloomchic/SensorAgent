# ProductCheckOutClick

## 基本信息

- **事件显示名**: 商品进入结算
- **事件英文名**: `ProductCheckOutClick`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页 | JavaScript | 购物车中点击CheckOut按钮时上报，每个商品SKU上报一条事件 | 2021.11.4 18:00后生效Customer also bought<br/>2021.11.8 12:00后生效搜索结果页 |  |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript |  |  |  |
| `cart_type` | 购物车类型 | STRING | 侧边栏展开购物车、完整页面购物车(/Cart) | JavaScript |  |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_sku` | 商品SKU | STRING | 当前商品SKU编号 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING |  | JavaScript |  |  |  |
| `product_url` | 商品URL | STRING | 当前商品链接 | JavaScript |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  | JavaScript |  |  |  |
