# 分区标签

收录社区分区（标签）及其侧边子标签相关的API接口

## 一览

| METHOD | URL                                 | COOKIE | 说明                                 |
| ------ | ----------------------------------- | ------ | ------------------------------------ |
| GET    | `/api/v1/tags`                      | 否     | [全部分区标签](./tag/list.md)        |
| GET    | `/api/v1/tags/{slug}/sidebar-links` | 否     | [分区侧边子标签](./tag/sidebar-links.md) |

> 全站共 9 个分区，`slug` 即[主题列表](./topic/list.md#主题列表)过滤时 `tag` 参数的值。
