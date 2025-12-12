# RulesClick

## 基本信息

- **事件显示名**: 点击规则条款
- **事件英文名**: `RulesClick`
- **所属模块**: 1.【首页】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript | 点击规则条款时上报 |  |  |
| `popup_type` | 弹窗类型 | INT | 7=带转盘前置弹窗版本（V1.2） | JavaScript |  |  |  |
| `click_item` | 点击位置 | INT | 1=ACTIVITY RULES<br/>2=TERMS<br/>3=PRIVACY POLICE | JavaScript |  |  |  |
