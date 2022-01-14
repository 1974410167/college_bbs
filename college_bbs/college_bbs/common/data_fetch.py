"""
用很少的数据库操作把数据从数据库中拿出来，然后在应用层进行赋值，避免循环中查询。

例如，要得到ParentComment关联的Topic中的name字段。
可以先从ParentComment表中post_id查询到Post表，
再根据Post表中的topic_id表查询Topic表，然后拿到Topic表中的对应数据

key为路径，帮助拿到对应的model, val为需要的值。
configs = {"post_id__topic_id": ["name"], "post_id": ["title", "topic_id"]}


"""
import importlib


class DataFetch:

    def __init__(self, objs, model, configs):
        self.objs = objs
        self.model = model
        self.configs = configs
        if not isinstance(self.objs, list):
            self.objs = [self.objs]

    def main_loop(self):
        """
        主循环
        """
        for key, fields in self.configs.items():
            constraint = self.model.ForeignKeyConstraint.fields
            forgn_list = key.split("__")
            depth = len(forgn_list)
            obj_linked = [self.objs]
            a = {}
            for item in self.objs:
                a[item["id"]] = item[forgn_list[0]]
            id_mapping_linked = [a]
            n = 0

            while True:
                foreign_id_str = forgn_list[n]
                cur_models = self.get_model(constraint, foreign_id_str)
                foreign_ids = self.get_foreign_ids(obj_linked, foreign_id_str)
                if n == depth-1:

                    fields.append("id")
                    q = cur_models.objects.filter(id__in=foreign_ids).values(*fields)
                    data = {}
                    for data_obj in q:
                        data_obj_id = data_obj["id"]
                        data[data_obj_id] = data_obj

                    key_name = forgn_list[0].split("_")[0]
                    for jj in forgn_list[1:]:
                        key_name += ("_" + jj.split("_")[0])
                    for obj1 in self.objs:
                        x = 0
                        cur_val = obj1["id"]
                        while True:
                            if x == depth-1:
                                cur_val = id_mapping_linked[x].get(cur_val)
                                need_data = data.get(cur_val)
                                obj1[key_name] = need_data
                                break
                            else:
                                cur_val = id_mapping_linked[x].get(cur_val)
                                x += 1
                    break
                else:
                    id_mapping = cur_models.objects.filter(id__in=foreign_ids).values("id", forgn_list[n+1])
                    obj_linked.append(id_mapping)
                    b = {}
                    for item in id_mapping:
                        b[item["id"]] = item[forgn_list[n+1]]
                    id_mapping_linked.append(b)
                    n += 1
                    constraint = cur_models.ForeignKeyConstraint.fields

    def get_foreign_ids(self, obj_linked, foreign_id):
        """
        得到外键列表
        """
        foreign_ids = []
        for obj in obj_linked[-1]:
            fign_id = obj.get(foreign_id)
            foreign_ids.append(fign_id)
        return foreign_ids

    def get_model(self, constraint, foreign_id):
        """
        根据外键字段和model中定义的ForeignKeyConstraint来动态加载model
        """
        model_msg = constraint.get(foreign_id)
        model_msg_ins = model_msg.get("to_model")
        path_list = model_msg_ins.split(".")
        model_path = path_list[0] + "." + "models"
        module_ins = importlib.import_module(model_path)
        class_ins = path_list[1]
        if hasattr(module_ins, class_ins):
            cur_models = getattr(module_ins, class_ins)
            return cur_models
        raise AttributeError(f"{module_ins} has not attribute {class_ins}")


user_configs = {"create_user_id": ["name"]}
