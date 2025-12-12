# ClickAddCartButton

## 基本信息

- **事件显示名**: 点击加入购物车（3.12版本新增）
- **事件英文名**: `ClickAddCartButton`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页、商详搭配Outfit浮层 | JavaScript | 点击加入购物车时上报 | 2021.11.4 18:00后生效Customer also bought<br/>2021.11.8 12:00后生效搜索结果页 |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_sku` | 商品SKU | STRING | 加入购物车的商品SKU编码 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING | 商品名称 | JavaScript |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `product_size` | 尺码 | STRING | 加入购物车的商品尺码 | JavaScript |  |  |  |
| `product_colour` | 颜色 | STRING | 加入购物车的商品颜色 |  |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 新增字段，类型<br/>- 非清仓：no_clearance<br/>- 清仓:clearance |  |  |  |  |
| `return_type` | 退货类型 | STRING | 退货政策：<br/>-可退：return<br/>-不可退：no_return |  |  |  |  |
| `recommend_size` |  | STRING | 推荐的尺码<br/>推荐成功 "10/M" ...<br/>其它没有推荐："" or NULL |  |  |  |  |
| `failed_reason` |  |  | 推荐失败的原因<br/>推荐成功："" or NULL<br/>品类不支持 "NotAvailable"<br/>没有登录 "Guest"<br/>没有填写胸围 "No Bust"<br/>没有合适尺码 "NoFitSize"<br/>其它没有推荐："Failed" | JavaScript |  |  |  |
