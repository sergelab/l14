import os
import networkx as nx

from uuid import uuid4


class PollsApi:
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'storage.json')

    def __init__(self):
        self.storage = self._load()

    def _get_next_question_id(self) -> int:
        return self.storage.number_of_nodes() + 1

    def _question_links(self, question_id):
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')

        edges = self.storage.edges(question_id, 'answer_id')
        return [dict(zip(['question_id', 'next_question_id', 'answer_id'], e)) for e in edges]

    def _find_answer(self, question_id, answer_id):
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')

        return answer_id in [a['id'] for a in self.storage.nodes(data=True)[question_id].get('answers', [])]

    def _make_edge(self, question_id, to_id, answer_id=None) -> bool:
        if not to_id or not question_id:
            return False
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')
        if to_id not in self.storage.nodes:
            raise Exception(f'Not found to_id = {to_id}')

        if answer_id and self._find_answer(question_id, answer_id):
            self.storage.add_edge(question_id, to_id, answer_id=answer_id)
            return True

        raise Exception(f'Not found answer_id = {answer_id}')

    def get_question(self, question_id):
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')

        d = self.storage.nodes(data=True)[question_id]
        ret_data = dict(d)
        ret_data.setdefault('id', question_id)
        ret_data.setdefault('links', self._question_links(question_id))
        return ret_data

    def get_all_questions(self) -> list:
        return [self.get_question(n) for n in self.storage.nodes]

    def add_question(self, data: dict):
        last_question_id = self.storage.number_of_nodes()
        q_id = self._get_next_question_id()

        data.setdefault('answers', [])
        self.storage.add_node(q_id, **data)

        if last_question_id > 0:
            self.storage.add_edge(last_question_id, q_id)

        self._save()

        ret_data = dict(data)
        ret_data.setdefault('id', q_id)
        return ret_data

    def update_question(self, question_id, data: dict):
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')

        data.pop('id', None)

        nx.set_node_attributes(self.storage, {question_id: data})
        self._save()
        return self.get_question(question_id)

    def add_answer(self, question_id, data: dict):
        if question_id not in self.storage.nodes:
            raise Exception(f'Not found question_id = {question_id}')

        q_data = self.storage.nodes(data=True)[question_id]
        q_data.setdefault('answers', [])

        a_id = str(uuid4())
        data.setdefault('id', a_id)

        q_data['answers'].append(data)
        nx.set_node_attributes(self.storage, q_data)
        self._make_edge(question_id, data.pop('next_question_id', None), answer_id=a_id)
        self._save()
        return a_id

    def update_answer(self, question_id, answer_id, data: dict):
        if self._find_answer(question_id, answer_id):
            ex_answer = self.storage.nodes(data=True)[question_id].get('answers', [])

            for an in ex_answer:
                if an['id'] == answer_id:
                    an.update(data)

            nx.set_node_attributes(self.storage, {question_id: {'answers': ex_answer}})
            self._make_edge(question_id, data.pop('next_question_id', None), answer_id)

            self._save()

        return question_id

    # Служебные методы

    def _load(self) -> nx.DiGraph:
        try:
            with open(self.STORAGE_FILE, 'r') as f:
                rs = nx.jit_graph(f.read(), create_using=nx.DiGraph())
                print('LOADED', rs)
                return rs
        except:
            return nx.DiGraph()

    def _save(self):
        with open(self.STORAGE_FILE, 'w') as f:
            f.write(nx.jit_data(self.storage))
