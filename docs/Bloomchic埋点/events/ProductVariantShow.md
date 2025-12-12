# ProductVariantShow

## 基本信息

- **事件显示名**: 商品Variant展示（3.21版本新增）
- **事件英文名**: `ProductVariantShow`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_page` | 来源页面 | STRING | 来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 |  |  |  |  |
| `from_module` | 来源模块 | STRING | 来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 |  |  |  |  |
| `page_code` | 当前页面 | STRING | 按照既定规则 上报page_code & module_name<br/>page_code:<br/>商详页的page_code：商详页<br/>微商详的page_code：打开微商详的当前页面 |  |  |  |  |
| `module_name` | 当前模块名称 | STRING | 按照既定规则 上报page_code & module_name<br/>module_name: 弹窗被认为主页面的模块，因此微商详弹窗应该上报 “微商详”<br/>商详页的module_name：商详页<br/>微商详的module_name：微商详 |  |  |  |  |
| `page_type` | 页面类型，"商详页"，"微商详"<br/>区分是否是微商详 | STRING | 商详页，微商详 |  |  |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 |  |  |  |  |
| `product_name` | 商品名称 | STRING |  |  |  |  |  |
| `product_sku` | 商品SKU | STRING | 选中的SKU编码 |  |  |  |  |
| `is_available` | 可用状态 | BOOL | 当前sku可售时上报false |  |  |  |  |
| `web_original_price` | 原价 | NUMBER | SKU原价 |  |  |  |  |
| `web_current_price` | 价格 | NUMBER | SKU当前售价 |  |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  |  |  |  |  |
| `product_size` | 尺码 | STRING | 选中的SKU的尺码名称 |  |  |  |  |
| `product_color` | 颜色 | STRING | 选中的SKU的颜色名称 |  |  |  |  |
| `product_colour（3.23之后移除）` | 颜色 | STRING | 选中的SKU的颜色名称 |  |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 当前SKU是否清仓商品<br/>- 非清仓：no_clearance<br/>- 清仓:clearance |  |  |  |  |
| `return_type` | 退货类型 | STRING | 当前SKU的退货政策：<br/>-可退：return<br/>-不可退：no_return<br/>如果是SPU级别的不可退,SKU延续SPU的政策 |  |  |  |  |
| `recommend_size` | 虚拟字段：combine_recommend_size | STRING | 推荐的尺码<br/>推荐成功 "10/M" ...<br/>其它没有推荐："" or NULL |  |  |  |  |
| `preorder_left_date` | SKUpre-order时间，距离发货天数 | NUMBER | APP 3.8版本新增<br/>距离预售日期还有几天，默认0 |  |  |  |  |
| `is_quickship_icon` | SKU是否有quickship标记 |  |  |  |  |  |  |
