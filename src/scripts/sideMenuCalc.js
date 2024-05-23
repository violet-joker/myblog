let options = []
export function menuCalc(topicList, articleList) {
    options = []
    // 先根据id从小到大排序，设置子目录的id小于父目录id
    topicList.sort((a, b) => a.topic_id - b.topic_id)
    for (let item of topicList) {
        // 插入根目录节点
        if (item.parent_id === null) {
            let data = new Node(item)
            options.push(data)
            continue
        }
        // 子目录
        for (let node of options)
            if (dfs(node, item)) break;
    }

    for (let item of articleList)
        for (let node of options)
            if (dfs(node, item)) break;
    console.log(options)
    return options
}

// 菜单节点的属性设置
function Node(data) {
    return {
        key: data.topic_id || data.article_id,
        label: data.title,
        children: null
    }
}

// dfs遍历options列表，查询匹配的父节点，并添加到children
function dfs(node, item) {
    if (item.parent_id === node.key || item.a_topic_id === node.key) {
        let data = new Node(item)
        node.children = node.children || []
        node.children.push(data)
        return true
    }
    if (node.children === null) return false
    for (let newNode of node.children) {
        if (dfs(newNode, item)) return true
    }
    return false
}