# BuildMyOutfitShow

## 基本信息

- **事件显示名**: 搭配推荐Build My Outfit展示
- **事件英文名**: `BuildMyOutfitShow`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_skc` | 商品SKC | STRING | 原商品skc |  | 商详页用户滑动到商详页第2张图时上报 | 商品搭配图功能 | 20230620.0 |
| `product_skc_list` | 商品SKC列表 | STRING | SKC1;SKC2;SKC3;推荐出的搭配skc，最多3个 |  |  |  | 20230620.0 |
| `product_spu` | 商品SPU | STRING | 原商品SPU编号 |  |  |  |  |
| `product_name` | 商品名称 | STRING | 原商品名称 |  |  |  |  |
