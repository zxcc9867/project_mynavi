

class ErrorMessages:
    def w01(self, arg1):
        return '登録されている' + arg1 + 'はありません。'

    def w02(self, arg1):
        return arg1 + 'は必須入力項目です。'

    def w03(self, arg1):
        return 'この' + arg1 + 'は既に使われています。'

    def w04(self, arg1):
        return arg1 + 'またはパスワードが誤っています。'

    def w05(self):
        return '「パスワード」と「パスワード（確認）」が一致しません。'

    def w06(self, arg1, arg2):
        return arg1 + 'は、' + arg2 + '文字で入力してください。'

    def w07(self, arg1, arg2):
        return arg1 + 'は、' + arg2 + '文字以内で入力してください。'

    def w08(self, arg1, arg2, arg3):
        return arg1 + 'は、' + arg2 + '文字から' + arg3 + '文字の範囲で入力してください。'

    def w09(self, arg1):
        return arg1 + 'は、半角文字で入力してください。'

    def w10(self, arg1):
        return arg1 + 'は、半角数字で入力してください。'

    def w11(self, arg1):
        return arg1 + 'は、半角英字で入力してください。'

    def w12(self, arg1):
        return arg1 + 'は、半角英数字で入力してください。'

    def w13(self, arg1):
        return arg1 + 'は、半角記号で入力してください。'

    def w14(self, arg1, arg2):
        return arg1 + 'は、' + arg2 + '形式で入力してください。'

    def w15(self, arg1):
        return arg1 + 'には、ログインが必要です。'

    def w16(self, arg1):
        return '検索条件に該当する' + arg1 + 'は登録されていません。'

    def w17(self):
        return '予約済みのチケットがある場合は退会できません。'


class InfoMessages:
    def i01(self, arg1):
        return arg1 + 'の登録が完了しました。'

    def i02(self, arg1):
        return arg1 + 'の変更が完了しました。'

    def i03(self, arg1):
        return arg1 + 'の削除が完了しました。'

    def i04(self):
        return '退会処理が完了しました。ご利用ありがとうございました。'

    def i05(self):
        return 'ログインしました。'
