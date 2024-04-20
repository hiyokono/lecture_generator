
import yaml
from graphviz import Digraph

# 英語版のシラバスデータ読み込みと処理
with open('syllabus.yaml', 'r') as file:
    syllabus_data_en = yaml.safe_load(file)

syllabus_en = syllabus_data_en['schedule']

g_en = Digraph(comment='Syllabus Graph')

for week_data in syllabus_en:
    week_index = syllabus_en.index(week_data)
    lectures = ', '.join(lecture['title'] for lecture in week_data['lectures'])
    week_node_name = f"Week {week_index + 1}\n{', '.join(week_data['topics'])}"
    g_en.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')

    with g_en.subgraph(name=f'cluster_week_{week_index + 1}') as sub:
        lecture_list = '\n'.join(lecture['title'] for lecture in week_data['lectures'])
        sub.node(f'lectures_{week_index + 1}', shape='box', label=lecture_list)
        g_en.edge(week_node_name, f'lectures_{week_index + 1}', style='dashed', tailport='s', headport='sw')

for i in range(len(syllabus_en) - 1):
    current_week = syllabus_en[i]
    next_week = syllabus_en[i + 1]
    current_week_node = f"Week {i + 1}\n{', '.join(current_week['topics'])}"
    next_week_node = f"Week {i + 2}\n{', '.join(next_week['topics'])}"
    g_en.edge(current_week_node, next_week_node)

g_en.render('syllabus_graph_en', format='png', view=True)

# 日本語版のシラバスデータ読み込みと処理
with open('syllabus_ja.yaml', 'r') as file:
    syllabus_data_ja = yaml.safe_load(file)

syllabus_ja = syllabus_data_ja['schedule']

g_ja = Digraph(comment='Syllabus Graph')

for week_data in syllabus_ja:
    week_index = syllabus_ja.index(week_data)
    lectures = ', '.join(lecture['title'] for lecture in week_data['lectures'])
    week_node_name = f"Week {week_index + 1}\n{', '.join(week_data['topics'])}"
    g_ja.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')

    with g_ja.subgraph(name=f'cluster_week_{week_index + 1}') as sub:
        lecture_list = '\n'.join(lecture['title'] for lecture in week_data['lectures'])
        sub.node(f'lectures_{week_index + 1}', shape='box', label=lecture_list)
        g_ja.edge(week_node_name, f'lectures_{week_index + 1}', style='dashed', tailport='s', headport='sw')

for i in range(len(syllabus_ja) - 1):
    current_week = syllabus_ja[i]
    next_week = syllabus_ja[i + 1]
    current_week_node = f"Week {i + 1}\n{', '.join(current_week['topics'])}"
    next_week_node = f"Week {i + 2}\n{', '.join(next_week['topics'])}"
    g_ja.edge(current_week_node, next_week_node)

g_ja.render('syllabus_graph_ja', format='png', view=True)
