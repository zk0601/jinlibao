from tornado.concurrent import run_on_executor
from .base import BaseHandler
import datetime
import traceback
import json

from models.user import User_Base, User_From, Spouse, Children, Phone_Name
from models.order import Order


class UserListHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            page = int(self.get_argument('page', 1))
            limit = int(self.get_argument('limit', 10))
            is_member = self.get_argument('is_member', None)
            has_deatil = self.get_argument('has_detail', None)

            time_format = "%Y-%m-%d %H:%M:%S"
            offset = limit * (page - 1)

            data = []
            users = self.session.query(User_Base).order_by(User_Base.create_time.asc()).limit(limit).offset(offset)
            for item in users:
                user = item.as_dict()
                user['create_time'] = item.create_time.strftime(time_format)

                phone = self.session.query(Phone_Name).filter(Phone_Name.openid == item.openid).first()
                if phone:
                    user['name'], user['phone'], user['wx_number'] = phone.name, phone.phone, phone.wx_number
                else:
                    user['name'], user['phone'], user['wx_number'] = '', '', ''

                order = self.session.query(Order).filter(Order.user_openid == item.openid, Order.pay_status == 2).first()
                if order:
                    user['is_member'] = 1
                else:
                    user['is_member'] = 0

                detail = self.session.query(User_From).filter(User_From.openid == item.openid).first()
                if detail:
                    user['has_detail'] = 1
                else:
                    user['has_detail'] = 0

                if is_member and is_member == 1:
                    if user['is_member'] == 0:
                        continue
                if has_deatil and has_deatil == 1:
                    if user['has_detail'] == 0:
                        continue
                data.append(user)

            return self.response(code=10001, msg='success', data=data)

        except Exception as e:
            self.logger.error(str(e.__traceback__.tb_lineno) + str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
        finally:
            self.session.remove()


class UserDeatilHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            openid = self.get_argument('openid', None)
            if not openid:
                return self.response(code=10002, msg='缺少openid')

            detail = self.session.query(User_From).filter(User_From.openid == openid).first()
            if not detail:
                return self.response(code=10002, msg='openid有误')

            data = dict()
            data['gender'] = detail.gender
            data['family'] = detail.family
            data['children_num'] = detail.children_num
            data['is_supportparents'] = detail.is_supportparents
            data['birthday'] = detail.birthday
            data['is_sick'] = detail.is_sick
            if detail.is_sick == 1:
                data['disease'] = detail.disease
            data['income'] = detail.income
            data['profession'] = detail.profession
            data['has_socialsecurity'] = detail.has_socialsecurity
            data['has_housloans'] = detail.has_housloans
            if detail.has_housloans == 1:
                data['houseloans_total'] = detail.houseloans_total
                data['houseloans_permonth'] = detail.houseloans_permonth
                data['houseloans_years'] = detail.houseloans_years
            data['has_carloans'] = detail.has_carloans
            if detail.has_carloans == 1:
                data['carloans_total'] = detail.carloans_total
                data['carloans_permonth'] = detail.carloans_permonth
                data['carloans_years'] = detail.carloans_years
            data['offen_businesstravel'] = detail.offen_businesstravel
            data['offen_car'] = detail.offen_car
            data['city'] = detail.city

            if detail.spouse_id != 0:
                spouse = self.session.query(Spouse).filter(Spouse.id == detail.spouse_id).first()
                s = dict()
                s['birthday'] = spouse.birthday
                s['is_sick'] = spouse.is_sick
                if spouse.is_sick == 1:
                    s['disease'] = spouse.disease
                s['income'] = spouse.income
                s['profession'] = spouse.profession
                s['has_socialsecurity'] = spouse.has_socialsecurity
                s['offen_businesstravel'] = spouse.offen_businesstravel
                s['offen_car'] = spouse.offen_car
                data['spouse'] = s

            def deal_child(child):
                c = dict()
                c['gender'] = child.gender
                c['birthday'] = child.birthday
                c['is_sick'] = child.is_sick
                if child.is_sick == 1:
                    c['disease'] = child.disease
                return c

            if detail.children_num != 0:
                children_list = []
                if detail.first_child_id != 0:
                    child = self.session.query(Children).filter(Children.id == detail.first_child_id).first()
                    children_list.append(deal_child(child))
                if detail.second_child_id != 0:
                    child = self.session.query(Children).filter(Children.id == detail.second_child_id).first()
                    children_list.append(deal_child(child))
                if detail.third_child_id != 0:
                    child = self.session.query(Children).filter(Children.id == detail.third_child_id).first()
                    children_list.append(deal_child(child))
                data['children'] = children_list

            return self.response(code=10001, msg='success', data=data)

        except Exception as e:
            self.logger.error(str(e.__traceback__.tb_lineno) + str(e))
            print(traceback.print_exc())
            return self.response(code=10000, msg='服务端异常')
        finally:
            self.session.remove()

