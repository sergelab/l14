import networkx as nx
import matplotlib as plt
from uuid import uuid4


GRAPH_FILE = 'graph.json'


def load() -> nx.DiGraph:
    try:
        with open(GRAPH_FILE, 'r') as f:
            return nx.jit_graph(f.read(), create_using=nx.DiGraph())
    except:
        return nx.DiGraph()


def save(g: nx.DiGraph):
    with open(GRAPH_FILE, 'w') as f:
        f.write(nx.jit_data(g))


def get_next_question_id(g: nx.DiGraph):
    return g.number_of_nodes() + 1


# data = {'title': str}
# output => question_id
# POST
def add_question(g: nx.DiGraph, data: dict):
    prev_id = g.number_of_nodes()
    q_id = get_next_question_id(g)

    new_data = data
    new_data.setdefault('answers', [])

    g.add_node(q_id, **new_data)

    if prev_id > 0:
        g.add_edge(prev_id, q_id)

    return q_id


def make_edge(g: nx.DiGraph, question_id, to_id, answer_id=None) -> bool:
    if not to_id or not question_id:
        return False
    if question_id not in g.nodes:
        raise Exception(f'Not found question_id = {question_id}')
    if to_id not in g.nodes:
        raise Exception(f'Not found to_id = {to_id}')

    if answer_id and find_answer(g, question_id, answer_id):
        g.add_edge(question_id, to_id, answer_id=answer_id)
        return True

    raise Exception(f'Not found answer_id = {answer_id}')


# POST
def add_answer(g: nx.DiGraph, question_id, data):
    if question_id not in g.nodes:
        raise Exception(f'Not found question id = {q_id}')

    q_data = g.nodes(data=True)[question_id]
    q_data.setdefault('answers', [])

    next_id = data.pop('next', None)
    a_id = str(uuid4())
    data.setdefault('id', a_id)

    q_data['answers'].append(data)
    nx.set_node_attributes(g, q_data)

    make_edge(g, question_id, next_id, answer_id=a_id)

    return a_id


def find_answer(g: nx.DiGraph, question_id, answer_id):
    if question_id not in g.nodes:
        raise Exception(f'Not found question id = {question_id}')
    return answer_id in [a['id'] for a in g.nodes(data=True)[question_id].get('answers', [])]


# PUT
def update_answer(g: nx.DiGraph, question_id, answer_id, data):
    if question_id not in g.nodes:
        raise Exception(f'Not found question id = {question_id}')

    if find_answer(g, question_id, answer_id):
        data.pop('id', None)
        title = data.pop('title', None)
        new_data = {}

        if title:
            new_data.setdefault('title', title)
            nx.set_node_attributes(g, {question_id: new_data})

        make_edge(g, question_id, data.pop('next', None), answer_id)

    else:
        raise Exception(f'Not found answer_id = {answer_id}')


# Возвращает следующий вопрос на основе текущего вопроса и выбранного ответа
# Если None — значит опрос закончен
def next_question(g: nx.DiGraph, current_question_id, answer_id):
    # Возвращает следующий вопрос
    edges = g.edges(current_question_id, 'answer_id')
    next_id = None

    for e in edges:
        if e[2] is not None:
            if e[2] == answer_id:
                return e[1]
        else:
            next_id = e[1]
    return next_id


def question_links(g: nx.DiGraph, question_id):
    edges = g.edges(question_id, 'answer_id')
    return [dict(zip(['q_id', 'next_q_id', 'answer_id'], e)) for e in edges]


def get_question(g: nx.DiGraph, question_id):
    if question_id not in g.nodes:
        raise Exception(f'Not found question_id {question_id}')

    d = g.nodes(data=True)[question_id]

    a = dict(d)
    a.setdefault('id', question_id)
    a.setdefault('links', question_links(g, question_id))

    return a


def run():
    g = load()

    q_id = add_question(g, {'title': 'Первый вопрос'})
    q2_id = add_question(g, {'title': 'Второй вопрос'})
    q3_id = add_question(g, {'title': 'Третий вопрос'})
    q4_id = add_question(g, {'title': 'вопрос 4'})
    q5_id = add_question(g, {'title': 'вопрос 5'})

    a11 = add_answer(g, q_id, {'title': 'Ответ 1-1'})
    a12 = add_answer(g, q_id, {'title': 'Ответ 1-2', 'next': q3_id})
    a13 = add_answer(g, q_id, {'title': 'Ответ 1-3', 'next': q5_id})

    a21 = add_answer(g, q2_id, {'title': 'Ответ 2-1'})
    a22 = add_answer(g, q2_id, {'title': 'Ответ 2-2'})

    # update_answer(g, 1, 'ac65f37d-97d7-4dd5-b8ce-e3fb8426c9fe', {'title': 'Ответ 1-2 ТЕСТ'})
    # update_answer(g, 2, '1a5b082f-6ab4-4a26-bfa0-0b58858e24d7', {'next': 5})

    for i in g.nodes(data=True):
        print(f'node = {i}')

    for i in g.edges(data=True):
        print(f'edge = {i}')

    # Получить ребра для текущего вопроса
    # print(g.out_edges(q_id, 'answer_id'))
    # print([i for i in nx.neighbors(g, 1)])

    # print(next_question(g, q_id, a11))
    # print(next_question(g, q_id, a12))

    # print(get_question(g, 1))

    # save(g)
    # Рисуем граф
    import matplotlib.pyplot as plt
    nx.draw_shell(g, with_labels=True)
    # nx.draw_spectral(g, with_labels=True)
    plt.show()
