# NavigationBarClick

## 基本信息

- **事件显示名**: 点击导航栏具体栏目
- **事件英文名**: `NavigationBarClick`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript | 点击导航栏具体栏目时上报 |  |  |
| `click_type` | 点击导航类型 | STRING | 比如一级导航、二级导航、三级导航 | JavaScript |  |  |  |
| `firstlevel_name` | 一级导航名称 | STRING | 比如点击 Dresses 则上报 Dresses | JavaScript |  |  |  |
| `secondlevel_name` | 二级导航名称 | STRING | 比如点击 Shop by color 则上报 Shop by color | JavaScript |  |  |  |
| `thirdlevel_name` | 三级导航名称 | STRING | 比如点击 White dresses 则上报 White dresses (品牌优化新上报) | JavaScript |  |  |  |
| `click_url` | 点击url | STRING | 点击url (品牌优化新上报) | JavaScript |  |  |  |
| `is_image_click` | 是否是图片点击 | BOOLEAN | 是否为配的图片点击 (品牌优化新上报) | JavaScript |  |  |  |
| `click_level` | 导航层级，对应导航类型 | NUMBER | 1,2,3 比如一级导航、二级导航、三级导航 (品牌优化新上报) | JavaScript |  |  |  |
| `is_go` | 是否跳转 | Boolean | 是否为跳转事件 | Javascript |  |  |  |
