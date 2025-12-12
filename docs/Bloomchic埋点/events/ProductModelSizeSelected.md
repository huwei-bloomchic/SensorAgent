# ProductModelSizeSelected

## 基本信息

- **事件显示名**: 点击下拉模特选择的选项
- **事件英文名**: `ProductModelSizeSelected`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页 |  |  | 220705牛仔项目添加 |  |
| `product_spu` | 商品SPU | STRING |  |  |  |  |  |
| `product_name` | 商品名称 | STRING |  |  |  |  |  |
| `model_id` | 选择模特的id |  | 元数据中的模特id，选项ALL的情况下显示ALL |  |  |  |  |
| `model_size` | 选择模特的尺码 |  | 元数据中的模特title，选项ALL的情况下显示展示值 |  |  |  |  |
