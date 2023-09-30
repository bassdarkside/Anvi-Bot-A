import telebot
from telebot import types, apihelper, util


# Function to read the token from a file
def read_token(filename):
    try:
        with open(filename, "r") as file:
            token = file.read().strip()
        return token
    except FileNotFoundError:
        raise Exception(
            f"File {filename} with the token "
            f"was not found. Make sure the file "
            f"exists and contains the bot token."
        )


# Reading the token from a file
TOKEN_FILE = "token_anvi_test.txt"
TOKEN = read_token(TOKEN_FILE)

bot = telebot.TeleBot(TOKEN)


catalog = {
    "chapter1": {
        "markup": "deodorants",
        "chapter_name": "Дезодорант (3)",
        "message": "Фізіологічні дезодоранти",
        "items": ["1", "2", "3"],
    },
    "chapter2": {
        "markup": "balms",
        "chapter_name": "Бальзам для губ (3)",
        "message": "Бальзами для губ і не тільки",
        "items": ["4", "5", "6"],
    },
    "chapter3": {
        "markup": "shampoo",
        "chapter_name": "Очищення (3)",
        "message": "Тверді шампуні",
        "items": ["7", "8", "9"],
    },
    "chapter4": {
        "markup": "care",
        "chapter_name": "Догляд (3)",
        "message": "Бальзами для волосся",
        "items": ["10", "11", "12"],
    },
    "chapter5": {
        "markup": "other",
        "chapter_name": "Інше",
        "message": "Інше",
        "items": ["13"],
    },
}

catalog_items = {
    "1": {
        "name": "Фізіологічний дезодорант SUN",
        "chapter": "chapter1",
        "price": "",
        "url": "",
        "description": "Фізіологічний дезодорат SUN Формула середньої інтенсивності,ідеально підійде для помірного потовиділення,одночасно мяка та дієва дія дезодоранту забезпечить комфотр та захист. SUN фізіологічний дезодорант Натуральний дезодорант, має природну антибактеріальну дію. Принцит його діі в запобіганні розмноженнюмікроорганізмів які спричиняютьнеприємний запах. не блокує потовіпротоки не порушує роботу потових залоз не перешкоджає фізіологічному процесу терморегуляції Переваги фізіологічних дезодорантів ANVI Суміш рослинно - мінералтьнихкомпонентів забезпечує відчуття сухості та впевненості протягом усього дня . Веганський , без жорстокості та без солі алюмінію Зволожуюча формула миттєво вбирається. На 100% не містить пластику та компостується. Стопи, лоб, груди - використовуйте всюди, де вам потрібен ефективний захист протягом усього дня. Однієї тубивистачає до 6 місяців.",
        "image": "https://static.wixstatic.com/media/626c22_6ec1b2baf2b6438e958adfd1b325be4e~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "2": {
        "name": "Фізіологічний дезодорант PURE",
        "chapter": "chapter1",
        "price": "",
        "url": "",
        "description": "Фізіологічний дезодорат PURE Особливо ніжна формула розробленаспеціально без використання ефірних олій та гідрокарбонат натрію.\n <b>Ідеально підійде для:</b>\n -Вагітних і годуючих мам.\n -Підлітків.\n -Тендітноі шкіри, шкіри схильноі до алергічних реакцій.\n Особлива формула дезодоранту ANVI PUREпоєднує ніжне піклування органічного олії кокоса першого холодного віджиму з дієвим антибактеріальним захистом природніх мінералів.\n Натуральний дезодорант, має природну антибактеріальну дію. Принцит його діі в запобіганні розмноженнюмікроорганізмів які спричиняютьнеприємний запах.\n Не блокує потовіпротоки не порушує роботу потових залоз не перешкоджає фізіологічному процесу терморегуляції.\n <b>Переваги фізіологічних дезодорантів ANVI</b>\n Суміш рослинних компонентів забезпечує відчуття сухості та впевненості протягом усього дня.\n Веганський, без жорстокості та без солі алюмінію Зволожуюча формула миттєво вбирається.\n На 100% не містить пластику та підлягає переробці.\n <b> Стопи, лоб, груди - використовуйте всюди,</b> де вам потрібен ефективний захист протягом усього дня Одного тюбика вистачає до 6 місяців.",
        "image": "https://static.wixstatic.com/media/626c22_5a5df9591a1d4cd6a2f36315c38fd41f~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "3": {
        "name": "Фізіологічний дезодорант FOREST",
        "chapter": "chapter1",
        "price": "",
        "url": "",
        "description": "Фізіологічний дезодорант rorest Натуральний дезодорант, має природну антибактеріальні властивості. Принцит його діі в запобіганні розмноженню мікроорганізмів які спричиняють неприємний запах. не блокує потові протоки не порушує роботу потових залоз не перешкоджає фізіологічному процесу терморегуляції Переваги фізіологічних дезодорантів ANVI Збагачена суміш першокласних, ароматних рослинних компонентів забезпечує відчуття сухості та впевненості протягом усього дня . Веганський , без жорстокості Без солей алюмінію Зволожуюча формула що миттєво вбирається. На 100% не містить пластику та придатний до компостування. Стопи, лоб, груди - використовуйте всюди, де вам потрібен ефективний захист протягом усього дня Одного тюбика вистачає до 6 місяців.",
        "image": "https://static.wixstatic.com/media/15e500_a9081b244820411088f896189c608271~mv2.jpeg/v1/fit/w_500,h_500,q_90/file.jpg",
    },
    "4": {
        "name": "Бальзам CITRUS",
        "chapter": "chapter2",
        "price": "",
        "url": "",
        "description": "Багатофункціональний бальзам -CITRUS з ефірною олією Сицилійського апельсина дарує життєрадісний цитрусовийаромат аолія шипшини , має потужний регенеруючий ефект. Використовуй його для губ і не тільки, кутикула, щічки,лікті-всюди де потрібний захист та живлення! Чудово захищає від морозу ,вітру, надмірної сухості повітря інших шкідливих факторів. Екологічне пакування з вторинно переробленого паперу придатне до компостування - наш спільний вклад в майбутнє планети! 100% рослинний склад 100% ручна робота 100% екологічне пакування 0 % пластику 0 % консервантів 0 % продуктів нафтопереробки",
        "image": "https://static.wixstatic.com/media/15e500_82e75b444b654f9087794cc44ec42073~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "5": {
        "name": "Бальзам MINT",
        "chapter": "chapter2",
        "price": "",
        "url": "",
        "description": "MINT багатофункціональний бальзам з ефірною олією м'яти та ментолом, дарує приємний холодок та збільшує яскравість твоїх вуст шляхом покрашення циркуляції крові! Бальзам має надзвичайно приємний ,свіжий аромат м'ятного льодяника! Використовуй його для губ і не тільки, кутикула, щічки,лікті-всюди де потрібний захист та живлення! Чудово захищає від морозу ,вітру, надмірної сухості повітря інших шкідливих факторів. Екологічне пакування з вторинно переробленого паперу придатне до компостування - наш спільний вклад в майбутнєпланети! 100% рослинний склад 100% ручна робота 100% екологічне пакування 0 % пластику 0 % консервантів 0 % продуктів нафтопереробки",
        "image": "https://static.wixstatic.com/media/15e500_b1932764b84b42f38a641af4fdadf28c~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg",
    },
    "6": {
        "name": "Бальзам COCO",
        "chapter": "chapter2",
        "price": "",
        "url": "",
        "description": "СОСО багатофункціональний бальзам на основі extra virgin кокосової олії ,що надає бальзаму неперевершений аромат далеких островів як в рекламі відомого батончика. Використовуй його для губ і не тільки, кутикула, щічки,лікті-всюди де потрібний захист та живлення! Чудово захищає від морозу ,вітру, надмірної сухості повітря інших шкідливих факторів,живить, підтримує ліпідний барʼєр, усуває тріщинки. Екологічне пакування з вторинно переробленого паперу придатне до компостування - наш спільний вклад в майбутнє планети! 100% рослинний склад 100% ручна робота 100% екологічне пакування 0 % пластику 0 % консервантів 0 % продуктів нафтопереробки Бальзам живить і захищає вуста від вітру, морозу, сухого повітря та інших факторів. Твої губки під надійним захистом! Ідеальний для діток та для тих хто полюбляє мінімалізм в ароматах.",
        "image": "https://static.wixstatic.com/media/15e500_d46a44c840d14c9191957b0baafc3277~mv2.jpg/v1/fit/w_500,h_500,q_90/file.jpg",
    },
    "7": {
        "name": "Фізіологічний шампуть VIRGIN",
        "chapter": "chapter3",
        "price": "",
        "url": "",
        "description": "Для створенняшампуню Virgin ми ретельно підібрали найкращі природні складові,що дбайливо очищають та допомагають в боротьбі з сухістю, заспокоютьчутливу шкіру голови надаючи волоссю м’якості та блиск. В основі твердих шампунів ANVI – м'які безсульфатні миючі речовини Sodium Cocoyl Isethionate,Sodium Methyl Oleoyl Taurate, отримані з рослинної сировини та повністю біорозкладні в природному середовищі. ANVI Virgin Для чутливої та схильної до сухості шкіри голови ,без запаху. Провітамін В5 відновлює ліпідну мантію Дівича олія кокосу глибоко живить та знімає подразнення Бетаін(рослинний полісахарид) -зволожує та кондиціонує Вітамін Е та протеїни пшениці -знижують трансепідермальну втрату вологи та зміцнює бар’єрну функцію. Переваги твердого шампуню: Має фізіологічний рівеньРН. Не пошкоджує ліпідний барєр,дружній до мікробіома Базується на безпечних, сертифікованих(EcoCert,COSMOS),миючих засобах. Концентрований та економний.Шматочок 100г замінює 3 пляшки рідкого шампуню. Відповідає принципам Zero Waste, не шкодить навколишньому середовищу.",
        "image": "https://static.wixstatic.com/media/626c22_83f2928502bc4e39b643aa566c17e321~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "8": {
        "name": "Фізіологічний шампуть WILD",
        "chapter": "chapter3",
        "price": "",
        "url": "",
        "description": "БЕЗ сульфатний шампунь WILDдля нормальної та схильної до жирності шкіри голови. Ми підібрали природні складові,що дбайливо очищають та допомагають в боротьбі з гіперактивність сальних залоз. Пудра кропивимає бактерицидну дію, бореться зі свербінням, зміцнює корені волосся Олія коноплі першого холодного віджиму- безцінний суперфуд для щкіри та волосся Зелена глина абсорбує надлишки себума Ментол покращує кровообіг,дарує відчуття прохолоди Цинк- мінарал що на клітинному рівні допомагає налагодити роботу сальних залоз Ефірна олія м’яти чинить протизапальну та дизинфікуючу діюз,німає відчуття втоми та роздратованість. Ефірна олія ялівцю має антибактеріальну дію та зміцнює фолікули. Протеїни пшениці -знижують трансепідермальну втрату вологи та зміцнює бар’єрну функцію. В основі шампунів ANVI– м'які безсульфатні миючі речовини Sodium Cocoyl Isethionate таCocamidopropyl Betaine, отримані з рослинної сировини та повністю біорозкладні в природному середовищі,зберігає здоровий захисний шар шкіри, на відміну від звичайного мила та сульфатних шампунів. Переваги твердого шампуню ANVI : Фізіологічний склад.Інгредієнти природного походження, що надзвичайно м’яко та дбайливо доглядають за шкірою та волоссям. Має фізіологічний рівень РН. Не пошкоджує ліпідний барєр,дружній до мікробіома. Концентрований та економний.Шматочок 100г замінює 3 пляшки рідкого шампуню. Екологічне пакування-Zero Waste, не шкодить навколишньому середовищу. Зручно брати в подорожі.Твердий шампунь не займає багато місця і не розливається у валізі. Не містить: -мила -води -сульфатів -SLS -силіконів -пластику",
        "image": "https://static.wixstatic.com/media/15e500_c5002c3e106a415a874e2a93d60329bf~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "9": {
        "name": "Фізіологічний шампуть PURE",
        "chapter": "chapter3",
        "price": "",
        "url": "",
        "description": "Для шампуню PURE ми підібрали найкращі природні складові,що дбайливо очищають, стимулює обмінні процеси, не пошкоджує ліпідну мантію, зволожують татонізують. Спіруліна -суперфуд та джерело вітамінів та мікроелементів Масло Какао -полірує та живить кутикулу волосся Рослинний кератин -відновлює волосяний стержень Ефірна олія лимону,нейролі та евкалипту покрашує настрій та надає волоссю супер блиск Екстракт окопника(аллантоїн) регенирує епідерміс,стабілізує роботу сальних залоз В основі шампунівANVI – м'які безсульфатні миючі речовини Sodium Cocoyl Isethionate таCocamidopropyl Betaine, отримані з рослинної сировини та повністю біорозкладні в природному середовищі. Шампунь має фізіологічний слабокислий рівень pH (5,5-6) і зберігає здоровий захисний шар шкіри, на відміну від звичайного мила та сульфатних шампунів. Переваги твердих шампунів ANVI: -Економна витрата, шматка вагою 80гр. врятує ві звалищя 2 пластикові пляшки! -Зручно брати в подорожі.Твердий шампунь не займає багато місця і не розливається у валізі. -Фізіологічний склад.Інгредієнти природного походження, що надзвичайно м’яко та дбайливо доглядають за шкірою та волоссям. -Екологічна упаковка придатна до компостування.",
        "image": "https://static.wixstatic.com/media/626c22_3529dae377b841e783211f09ea0c5c5b~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "10": {
        "name": "Захисна сироватка GLOW",
        "chapter": "chapter4",
        "price": "",
        "url": "",
        "description": "Захисна сироватка glow Новий інноваційний екологічний продукт по догляду за волоссям. Високоінтенсивний догляд-покрашує структуру волосини глибоко з середини,живить та наповнює цінними рослинними компонентами. 100% рослинний склад,без силіконів Поєднання цінних олій та емолентів у “сухій” олійці для волосся дарує миттевий ефект сяяння та розгладження на поверхні волосини тапролонговану дію в кортексі. Сироватка для всіх типів волосся,особливо для схильного до ламкості, сухого та пористог. • Живить і запечатує зневоднені та пошкоджені кінчики • Захищає кінчики від негативного впливу зовнішніх факторів • Підходить для волосся будь якої будь-якої довжини та текстури • Миттєво надає блиску,та розплутує • Полірує кутикулу та зберігає контроль над завитками. • Волосся залишається м'яким і шовковистим. Результат: ущільнення кінчиків ,блискуче,гладке та відновденеволосся.",
        "image": "https://static.wixstatic.com/media/626c22_4d8c793b09af4d899d3033c6dc91f78d~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "11": {
        "name": "SHINE твердий бальзам кондиціонер",
        "chapter": "chapter4",
        "price": "",
        "url": "",
        "description": "SHINE твердий кондиціонер, який полірує кутикулуволосся,дарує блиск і гладкість. Результат живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Він містить цінні та корисні: оліїконоплі, зародків пшениці, кокосу, стероли гірчиці, пантенол та вітамін Е. Ніжно огортає кожну волосинку цінними ліпідами,закриває лусочки кутикули і твоє волосся стає міцнішим,легшим у догляді та захищеним від негативних факторів зовнішнього середовища. ANVI –дієвий високоінтенсивний доглядза волоссям, а не просто Zero Waste альтернатива. Завдяки новітнім досягненням в розробці екологічної косметики нам вдалося створити багатофункціональний продукт що замінює мінімум три звичайні продукти для волосся. Кондиціонер Маска Незмивний засіб для кінчиків Живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Жодного зайвого чи не етичного компонента: Купуючи засоби догляду ANVIтипідтримуєшУкраїнське виробництво, етичне використання природних ресурсів,скорочення кількості відходів та піклуєшся про себе та планету.",
        "image": "https://static.wixstatic.com/media/626c22_304a58304091435aa6b2b77e4d30c4a2~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "12": {
        "name": "SILK твердий бальзам кондиціонер",
        "chapter": "chapter4",
        "price": "",
        "url": "",
        "description": "SILK- твердий кондиціонер, який ідеально розплутує волосся, та надастьблиск і гладкість. Він містить багато кориснихдля волосся олій авокадо,брокколіта какао, амінокислоти пшениці,пантенол та вітамін Е. Ніжно огортає кожну волосинку цінними ліпідами,закриває лусочки кутикули і твоє волосся стає міцнішим,легшим у догляді та захищеним від негативних факторів зовнішнього середовища. Без краплі силіконів та барвників,віддущок,та інщих непотрібних тобі та природі компонентів. Твердий кондиціонер ANVI –дієвий високоінтенсивний доглядза волоссям, а не просто Zero Waste альтернатива. Завдяки новітнім досягненням в розробці екологічної косметики нам вдалося створити багатофункціональний продукт що замінює мінімум три звичайні продукти для волосся. Кондиціонер Маска Незмивний засіб для кінчиків Живе, еластичне та доглянуте волосся без обтяження. Чудово знімає статичний заряд та полегшує розчісування. Жодного зайвого чи не етичного компонента: Купуючи засоби догляду ANVIтипідтримуєшУкраїнське виробництво, етичне використання природних ресурсів,скорочення кількості відходів та піклуєшся про себе та планету.",
        "image": "https://static.wixstatic.com/media/626c22_489161c6883d49989db2b99923af0c2c~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
    "13": {
        "name": "Крем-ліпід для рук та тіла з екстрактами зернових.",
        "chapter": "chapter5",
        "price": "",
        "url": "",
        "description": "Крем-ліпід для рук та тіла з екстрактами зернових. Живильний та лагідний . Крем з комплексом екстрактів «Українськи злаків» що лягідно доглядає, відновлює ліпідний барєр . Вбирається за лічені секунди, зволожує на цілий день. Наш крафтовий продукт, виготовлений з уважністю до людини та природи, відповідально і чесно. Крем має приємний оксамитовий дотик і пудровий ефект після нанесення та містить екстракт вівса та олію пшениці для заспокоєння шкіри. Вівсяний порошок, що входить до складу, забезпечує зволоження і загоєння, а бета-глюкан та авенантраміди (це поліфенол, потужний антиоксидант, присутній лише у зовнішньому шарі зерна вівса) мають протизапальні та антиоксидантні властивості. Білки, складні вуглеводи та ліпіди, які живлять і зволожують шкіру, забезпечуючивідновленнязахисногобар'єру тазволоження найсухіших ділянокшкіризабезпечуючи відчуття комфортудля всього тіла. Наш крафтовий продукт, виготовлений з уважністю до людини та природи, відповідально і чесно.",
        "image": "https://static.wixstatic.com/media/15e500_09bcbf1a797b41d4b9b579de351f6c1d~mv2.png/v1/fit/w_500,h_500,q_90/file.png",
    },
}


# Reply Buttons
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📒 Каталог")
    btn2 = types.KeyboardButton("🛍️ Кошик")
    btn3 = types.KeyboardButton("🥑 Корисності")

    markup.row(btn1, btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "Hi, {0.first_name}!".format(message.from_user),
        reply_markup=markup,
    )


# Reply on Catalog button click
@bot.message_handler()
def check_reply(message: types.Message):
    if message.text == "📒 Каталог":
        markup = types.InlineKeyboardMarkup()
        for chapter in catalog.keys():
            name = catalog[chapter]["chapter_name"]
            button = chapter
            button = types.InlineKeyboardButton(name, callback_data=chapter)
            markup.row(button)
        bot.send_message(
            message.chat.id, "Дивись, що в нас є 🥰", reply_markup=markup
        )


# Chapter -> Items (InlineButtons menu updating)
@bot.callback_query_handler(func=lambda callback: True)
def callback_chapter(callback):
    from .catalog import read_catalog_from_file

    catalog_items = read_catalog_from_file()
    # go to chapter
    if callback.data in catalog.keys():
        for callback_data_catalog in catalog.keys():
            if callback.data == callback_data_catalog:
                items = catalog[callback_data_catalog]["items"]
                message = catalog[callback_data_catalog]["message"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)
                bot.edit_message_text(
                    message,
                    callback.message.chat.id,
                    callback.message.message_id,
                    reply_markup=markup,
                )
    # go to item page
    elif callback.data in catalog_items.keys():
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if callback.data == id:
                chapter = catalog_items[id]["chapter"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до категорії",
                    callback_data=f"back_to_chapter_{chapter}",
                )
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_price = catalog_items[id]["price"]
                id_description = str(id) + "_description"
                description = types.InlineKeyboardButton(
                    "Опис продукту", callback_data=f"{id}_description"
                )
                add_to_cart = types.InlineKeyboardButton(
                    "Додати у кошик", callback_data="cart"
                )
                sum = types.InlineKeyboardButton(
                    item_price, callback_data="sum"
                )
                markup.row(description)
                markup.row(add_to_cart)
                markup.row(sum)
                markup.row(back)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_photo(
                    callback.message.chat.id,
                    item_image,
                    caption=item_name,
                    reply_markup=markup,
                )
    # go to item description
    elif callback.data.endswith("_description"):
        item_id = callback.data.replace("_description", "")
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if item_id == id:
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_description = catalog_items[id]["description"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до продукту",
                    callback_data=f"back_to_item_{item_id}",
                )
                markup.row(back)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_photo(
                    callback.message.chat.id, item_image, caption=item_name
                )
                for description in util.split_string(item_description, 3000):
                    bot.send_message(
                        callback.message.chat.id,
                        item_description,
                        parse_mode="HTML",
                        reply_markup=markup,
                    )
    # back description -> item (the description message is left)
    elif callback.data.startswith("back_to_item_"):
        item_id = callback.data.replace("back_to_item_", "")
        markup = types.InlineKeyboardMarkup()
        for id in catalog_items.keys():
            if item_id == id:
                chapter = catalog_items[id]["chapter"]
                back = types.InlineKeyboardButton(
                    "⬅️ Назад до категорії",
                    callback_data=f"back_to_chapter_{chapter}",
                )
                item_name = catalog_items[id]["name"]
                item_image = catalog_items[id]["image"]
                item_price = catalog_items[id]["price"]
                description = types.InlineKeyboardButton(
                    "Опис продукту", callback_data=f"{id}_description"
                )
                add_to_cart = types.InlineKeyboardButton(
                    "Додати у кошик", callback_data="cart"
                )
                sum = types.InlineKeyboardButton(
                    item_price, callback_data="sum"
                )
                markup.row(description)
                markup.row(add_to_cart)
                markup.row(sum)
                markup.row(back)
                bot.send_photo(
                    callback.message.chat.id,
                    item_image,
                    caption=item_name,
                    reply_markup=markup,
                )
    # back item -> chapter
    elif callback.data.startswith("back_to_chapter_"):
        chapter = callback.data.replace("back_to_chapter_", "")
        markup = types.InlineKeyboardMarkup()
        for chapter_catalog in catalog.keys():
            if chapter_catalog == chapter:
                items = catalog[chapter]["items"]
                message = catalog[chapter]["message"]
                markup = types.InlineKeyboardMarkup()
                for item in items:
                    item_name = catalog_items[item]["name"]
                    item_id = item
                    button = types.InlineKeyboardButton(
                        item_name, callback_data=item_id
                    )
                    markup.row(button)
                bot.delete_message(
                    callback.message.chat.id, callback.message.message_id
                )
                bot.send_message(
                    callback.message.chat.id, message, reply_markup=markup
                )


# Starting the bot
def bot_run():
    try:
        print("Bot starting..")
        apihelper.SESSION_TIME_TO_LIVE = 5 * 60
        apihelper.RETRY_ON_ERROR = True
        bot.infinity_polling()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    bot_run()
