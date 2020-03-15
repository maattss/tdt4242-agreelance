def setup(self):
        # nominal values
        # ProjectCategory(name="Test").save()
        for x in range(500):
            ProjectCategory(name=x).save()

    def test_form(self):
        data = {'username': 'test', 'first_name': "Test", 'last_name': "Test",
                'categories': [ProjectCategory.objects.get(name=0)], 'company': "Test",
                'email': "test@test.com", 'email_confirmation': "test@test.com",
                'password1': "qwertyuiopå", 'password2': "qwertyuiopå",
                'phone_number': "123456", 'street_address': "TestVeien 1",
                'city': "Test", 'state': "Test", 'postal_code': "1234",
                'country': 'Test'}
        form = SignUpForm(data)
        print(form.errors)
        print(form.non_field_errors())
        self.assertTrue(form.is_valid())

    def test_bounds(self):
        # Character sets for generating strings
        alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        num = "1234567890"
        sym = "@£$€{[]}!#¤%&/()=?|*ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω"
        alls = alph + num + sym
        unamesym = "@.+-_"

        # Boundary values for num of chars in fields
        max_name = 150
        min_name = 1
        max_pass = 4096
        min_pass = 8
        max_o = 50
        max_o2 = 30
        min_o = 1

        def rand_test(inputs):

            # Set everything to min length
            data = {'username': get_random_string(min_name, alph + unamesym + num),
                    'first_name': get_random_string(min_o, alls),
                    'last_name': get_random_string(min_o, alls),
                    'categories': [ProjectCategory.objects.get(name=0)],
                    'company': "",
                    'email': get_random_string(1) + "@" + get_random_string(1) +
                             "." + get_random_string(2),
                    'email_confirmation': get_random_string(1) + "@" + get_random_string(1) +
                                          "." + get_random_string(2),
                    'password1': get_random_string(min_pass, alls),
                    'phone_number': get_random_string(min_o, alls),
                    'street_address': get_random_string(min_o, alls),
                    'city': get_random_string(min_o, alls),
                    'state': get_random_string(min_o, alls),
                    'postal_code': get_random_string(min_o, alls),
                    'country': get_random_string(min_o, alls)}

            # Set chosen to length
            if inputs[0] == 1:
                data['username'] = get_random_string(max_name, alph + unamesym + num)
            if inputs[1] == 1:
                data['first_name'] = get_random_string(max_o2, alph + num)
            if inputs[2] == 1:
                data['last_name'] = get_random_string(max_o2, alph + unamesym + num)
            if inputs[3] == 1:
                data['categories'] = ProjectCategory.objects.all()
            if inputs[4] == 1:
                data['company'] = get_random_string(max_o2, alph + num)
            if inputs[5] == 1:
                data['email'] = get_random_string(126) + "@" + get_random_string(63) + "." + get_random_string(63)
            if inputs[6] == 1:
                data['email_confirmation'] = get_random_string(126) + "@" + get_random_string(63) + "." + get_random_string(63)
            if inputs[7] == 1:
                data['password1'] = get_random_string(max_pass, alph + num + sym)
            data['password2'] = data['password1']
            if inputs[8] == 1:
                data['phone_number'] = get_random_string(max_o, alph + num)
            if inputs[9] == 1:
                data['street_address'] = get_random_string(max_o, alph + num)
            if inputs[10] == 1:
                data['city'] = get_random_string(max_o, alph + num)
            if inputs[11] == 1:
                data['state'] = get_random_string(max_o, alph + num)
            if inputs[12] == 1:
                data['postal_code'] = get_random_string(max_o, alph + num)
            if inputs[13] == 1:
                data['country'] = get_random_string(max_o, alph + num)

            # data['username'] =
            # data['password1'] = get_random_string(pwd_length, chars_uname + extra_chars_pwd)
            form = SignUpForm(data)

            while "too similar" in form.errors:
                print(form.errors)
                print(data)
                if inputs[7] == 1:
                    data['password1'] = get_random_string(max_pass, alph + num + sym)
                else:
                    data['password1'] = get_random_string(min_pass, alph + num + sym)
                data['password2'] = data['password1']
                form = SignUpForm(data)

            success = form.is_valid()

            if not success:
                print("USER:", data)
                print()
                print("ERRORS")
                print(form.errors)
                print()
                print("NFERRORS:")
                print(form.non_field_errors())
                print()
                print("MINMAX:")
                print(inputs)
                print()

            self.assertTrue(success)

        for x in itertools.product([0, 1], repeat=14):
            rand_test(x)
