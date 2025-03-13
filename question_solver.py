from openai import OpenAI

with open('../openai_api_key.env', 'r') as file:
    openai_api_key = file.read().replace('\n', '')
client = OpenAI(api_key=openai_api_key)


def solve_question(question: str, user_profile: str, document: str, language: str) -> str:
    # Construct the prompt by combining all inputs.
    prompt = (
        "You are given a document, a question asked by a user and a user profile."
        "The user profile describe the specific profile and intent of the user in related to the question and the text."
        "You are tasked to answer the question given the user profile directly.\n"
        f"The answer should be in {language}"
        f"Question:{question}\n"
        f"User Profile:{user_profile}\n"
        "Document:\n"
        f"{document}\n\n"
    )

    # Call the OpenAI API to generate a response.
    model_name = "gpt-4o"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.7,
        frequency_penalty=0,
        presence_penalty=0
    )

    output = response.choices[0].message.content

    return output


# Example usage:
if __name__ == "__main__":
    question = "כמה ימי חופשת לידה מגיעים לי אם נולד לי ילד?"
    user_profile = "המשתמש הוא אב. האם מעוניינת לחלוק את חופשת הלידה עם האב. לא חלפו שישה שבועות מהלידה, והמשתמש לא מבקש חופשה חופפת עם היולדת. האם מסוגלת לטפל בתינוק."
    document = """
    # חופשת לידה (תקופת לידה והורות) (זכות) – כל-זכות
עובדות שעבדו לפחות שנה רצופה אצל המעסיק או באותו מקום עבודה, זכאיות לחופשת לידה (תקופת לידה והורות) של 26 שבועות (שרק חלק ממנה הוא בתשלום)

עובדות שעבדו פחות מ-12 חודשים אצל אותו מעסיק זכאיות לחופשת לידה של 15 שבועות (שחלקה או כולה בתשלום, בהתאם לתנאי הזכאות של דמי לידה)

הזכאות לתשלום דמי לידה (לעובד/ת שכיר/ה או עצמאי/ת) נקבעת בהתאם לתקופה שהעובד/ת שילמ/ה דמי ביטוח לאומי

מעסיק אינו רשאי למנוע מעובד/ת לצאת לחופשת לידה, או לפטר עובד/ת במהלך החופשה ולמשך 60 יום לאחריה

בקצרה
-----

דף זה עוסק בחופשת לידה ולא בדמי לידה

המידע מתייחס למשך חופשת הלידה שבה מותר לעובד/ת להיעדר מהעבודה בשל הלידה (בהתאם לחוק עבודת נשים).  
דף נפרד - דמי לידה, עוסק בתקופה שבה משולמים לעובד/ת (שכיר/ה או עצמאי/ת) דמי לידה מהמוסד לביטוח לאומי.

עובדת שעבדה **12 חודשים לפחות** ברציפות אצל אותו מעסיק או באותו מקום עבודה, זכאית ל**חופשת לידה (תקופת לידה והורות) של 26 שבועות**.

*   עובדת שעבדה **פחות מ-12 חודשים** אצל אותו מעסיק או באותו מקום עבודה, זכאית לחופשת לידה של 15 שבועות.
*   כל עובדת רשאית, אם היא רוצה בכך וללא כל תנאי , להתחיל את חופשת הלידה 7 שבועות (או פחות מזה) לפני יום הלידה המשוער ואת שאר השבועות אחרי יום הלידה. גם במקרה זה משך כל חופשת הלידה לא יעלה על 26 שבועות או 15 שבועות בהתאם לתקופת ההעסקה של העובדת.
*   חשוב להדגיש: רק עבור חלק מהחופשה ניתן תשלום מהמוסד לביטוח לאומי. למידע נוסף ראו דמי לידה.
*   היולדת רשאית לחלוק את חופשת הלידה עם בן הזוג. לפרטים נוספים ראו חופשת לידה לבן זוג של יולדת.
*   במהלך חופשת הלידה העובד/ת ממשיכ/ה לצבור זכויות סוציאליות שמוקנות על-פי הוותק במקום העבודה (ראו פרטים בהמשך).
*   **במהלך חופשת הלידה אסור למעסיק להעסיק את העובדת או העובד**, גם אם העובדת או העובד הם אלה שביקשו לעבוד מרצונם. לקריאת פסק דין בסוגיה זו לחצו כאן.
*   כל עובדת רשאית לקחת חופשה ללא תשלום (חל"ת) בתום חופשת הלידה באורך של רבע מתקופת עבודתה אצל אותו מעסיק או באותו מקום עבודה עד שנה מיום הלידה, שבמהלכה ובמשך 60 יום מסיומה אסור לפטר אותה.

מי זכאי?
--------

### עובדת שכירה שילדה

*   עובדת שעבדה **12 חודשים לפחות** אצל אותו מעסיק או באותו מקום עבודה, זכאית ל**חופשת לידה של 26 שבועות**.
*   עובדת שעבדה **פחות מ-12 חודשים** אצל אותו מעסיק או באותו מקום עבודה זכאית ל**חופשת לידה של 15 שבועות** (בלידות שאירעו לפני 01.01.2017, הזכאות הייתה לחופשת לידה של 14 שבועות).
*   עובדת זכאית לחופשת לידה גם אם העובר/התינוק נפטר לאחר הלידה.
*   סעיף 39 לחוק הביטוח הלאומי מגדיר "לידה" כלידת ולד חי (בכל אחד משבועות ההיריון) או לידה אחרי 22 שבועות של היריון.
    *   בהתאם לכך, הפרשנות המקובלת היא שנשים שעברו הפלה או הפסקת היריון אחרי 22 שבועות נחשבות כנשים שילדו, והן זכאיות לזכויות והגנות חוקיות כמו נשים שילדו תינוק חי. למידע על זכויות במקרה כזה ראו זכותון ליולדת שעברה לידה שקטה ולבן/בת זוגה.
    *   למידע לגבי הפלה שאירעה לפני שחלפו 22 שבועות של היריון, ראו זכויות תעסוקה לאחר הפלה.

### בן הזוג של היולדת

*   בן זוג של יולדת זכאי לצאת לחופשת לידה במקרים הבאים:
    *   כאשר היולדת בוחרת לקצר את חופשת הלידה שלה, ובן הזוג מחליף אותה בתקופה שנותרה מתום 6 השבועות הראשונים אחרי יום הלידה.
    *   כאשר היולדת מוותרת על תשלום דמי לידה עבור השבוע האחרון שבו הייתה זכאית להם ובן הזוג יוצא לחופשת לידה בת שבוע **במקביל** לחופשת הלידה של היולדת.
    *   כאשר היולדת לא מסוגלת לטפל בתינוק בגלל נכות או מחלה, ובן הזוג נמצא עמו ומטפל בו.
*   למידע נוסף ראו חופשת לידה לבן זוג של יולדת.

### אוכלוסיות נוספות

*   הורים מאמצים - למידע נוסף ראו חופשת לידה להורה מאמץ (חופשת אימוץ) "חופשת לידה להורה מאמץ (חופשת אימוץ)").
*   הורים המקבלים תינוק למשמורת מאם פונדקאית - למידע נוסף ראו חופשת לידה להורה מיועד לפי חוק הסכמים לנשיאת עוברים (פונדקאות) "חופשת לידה להורה מיועד לפי חוק הסכמים לנשיאת עוברים (פונדקאות)").
*   הורים שקיבלו לאומנה ילד שגילו עד 10 שנים, לתקופה העולה על 6 חודשים - למידע נוסף ראו חופשת לידה להורים במשפחת אומנה (חופשת אומנה) "חופשת לידה להורים במשפחת אומנה (חופשת אומנה)").

תשלום דמי לידה במהלך חופשת הלידה
--------------------------------

*   במהלך חופשת הלידה העובדת לא זכאית לתשלום שכר, אולם **בחלק מהתקופה** היא זכאית לתשלום **דמי לידה מהמוסד לביטוח לאומי**, בהתאם לתקופה ששולמו עבורה דמי ביטוח לאומי:
    *   מי ששילמה דמי ביטוח לאומי עבור 10 חודשים מתוך 14 החודשים שקדמו ליציאתה לחופשת לידה, או 15 חודשים מתוך 22 החודשים שקדמו ליציאתה לחופשת לידה, זכאית לדמי לידה במשך **15** שבועות מתוך חופשת הלידה (בלידות שאירעו לפני ה-01.01.2017, הזכאות לדמי לידה הייתה במשך 14 שבועות).
    *   מי ששילמה דמי ביטוח לאומי עבור 6 חודשים מתוך 14 החודשים שקדמו ליציאתה לחופשת לידה זכאית לדמי לידה במשך **8** שבועות מתוך חופשת הלידה (בלידות שאירעו לפני 01.01.2017, הזכאות לדמי לידה הייתה במשך 7 שבועות).
*   העובדת אינה זכאית לכל תשלום או דמי לידה עבור השבועות הנותרים של חופשת הלידה, אולם היא ממשיכה לצבור זכויות סוציאליות שמקורן בוותק במקום העבודה במהלך השבועות הללו.

*   עובדת שעבדה שנה ו-3 חודשים במקום העבודה זכאית לחופשת לידה למשך 26 שבועות.
*   העובדת שילמה דמי ביטוח לאומי עבור 15 חודשים מתוך 22 החודשים שקדמו ליציאתה לחופשת לידה.
*   עבור 15 שבועות מתוך 26 השבועות של חופשת הלידה ישולמו לה דמי לידה. 11 השבועות הנותרים יהיו בלי תשלום.

*   עובדת שעבדה 6 חודשים במקום העבודה זכאית לחופשת לידה למשך 15 שבועות.
*   העובדת שילמה דמי ביטוח לאומי עבור 6 חודשים מתוך 14 החודשים שקדמו ליציאתה לחופשת לידה.
*   עבור 8 שבועות מתוך 15 השבועות של חופשת הלידה ישולמו לה דמי לידה. 7 השבועות הנותרים יהיו בלי תשלום.

*   עובדת שעבדה 10 חודשים במקום העבודה זכאית לחופשת לידה למשך 15 שבועות.
*   העובדת שילמה דמי ביטוח לאומי עבור 10 חודשים מתוך 14 החודשים שקדמו ליציאתה לחופשת לידה.
*   היא תהיה זכאית לתשלום דמי לידה עבור כל 15 השבועות של חופשת הלידה.

*   **למידע נוסף על הזכאות ואופן חישוב התשלום, ראו דמי לידה.**

קיצור חופשת הלידה
-----------------

*   עובדת שעבדה 12 חודשים לפחות זכאית לקצר את חופשת הלידה, בתנאי שחופשת הלידה שלה לא תפחת מ-15 שבועות.
    *   מעסיק שקיבל מעובדת הודעה על רצונה לקצר את חופשת הלידה, לא יוכל לדחות את חזרתה לעבודה למשך יותר מ-3 שבועות.

עובדת המעוניינת לשוב לעבודה בתום 15 השבועות של חופשת הלידה שהם בתשלום, צריכה להודיע על כך למעסיק כבר בשבוע ה-12 של חופשת הלידה, כך שחזרתה לא תידחה למשך יותר מ-3 שבועות).

*   למרות זאת, עובדת רשאית לקצר את חופשה הלידה ולחזור לעבודה מוקדם יותר, כבר בתום 6 שבועות מיום הלידה (או מאוחר יותר), אם בן זוגה מחליף אותה ביתרת חופשת הלידה שנותרה ושלא נוצלה על ידה.
    *   במקרה שעובדת בחרה לקצר את חופשת הלידה ולחזור לעבודה, בן זוגה רשאי לחלוק עימה את חופשת הלידה (אותו חלק שבת הזוג לא ניצלה) החל מהשבוע השביעי ללידה. כדי שבן הזוג יהיה זכאי לדמי לידה בתקופה זו הוא חייב לשהות בחופשת לידה במשך 7 ימים לפחות (למידע נוסף ראו דמי לידה לבן זוג של יולדת).
    *   זכות זו מוענקת לכל עובדת שיצאה לחופשת לידה, בלי קשר לוותק שלה במקום העבודה ובלי קשר למשך התקופה שבה היא זכאית לדמי לידה (כלומר גם מי שזכאית לחופשת לידה של 26 שבועות וגם מי שזכאית לחופשת לידה של 15 שבועות, גם מי שזכאית לדמי לידה במשך 15 שבועות וגם מי שזכאית לדמי לידה במשך 8 שבועות).
    *   למידע נוסף ראו חופשת לידה לבן זוג של יולדת.

*   כמו כן, עובדת הזכאית לדמי לידה עבור 15 שבועות ובן זוגה יוצא לחופשת לידה בשבוע האחרון שבו היא זכאית לדמי לידה, רשאית לחזור לעבודתה במהלך שבוע זה (כלומר אחרי 14 שבועות של חופשה) בתנאי שהיא מוותרת על דמי הלידה עבור אותו שבוע.
    *   היולדת רשאית להישאר בחופשת לידה במהלך שבוע זה במקביל לבן זוגה (מבלי שתהיה זכאית לדמי לידה באותו שבוע).
    *   אם היא זכאית לדמי לידה במשך 8 שבועות, היא **אינה** רשאית לקצר את החופשה ולא תוכל לחזור לעבודה לפני תום 15 שבועות של חופשת לידה.
    *   למידע נוסף ראו חופשת לידה לבן זוג של יולדת.
*   בנוסף, במקרים הבאים מותר לקצר את חופשת הלידה, **בהסכמת העובדת ובאישור בכתב מרופא**, בתנאי שהחופשה תכלול לפחות 3 שבועות אחרי הלידה:
    *   במקרה שהנולד אינו בחיים (למשל: נפטר לאחר הלידה או נולד בלידה שקטה).
    *   במקרה שהיולדת הסכימה שהתינוק יאומץ, או שהיא אם פונדקאית, וזאת בתנאי שבתוך 14 ימים מהלידה העובדת מסרה למעסיק הודעה בכתב לגבי הסכמתה לקצר את חופשת הלידה, וציינה את המועד שבו בכוונתה לסיים את החופשה.

הארכת חופשת הלידה
-----------------

### לידה רב עוברית

*   **יולדת שילדה באותה לידה יותר מתינוק אחד**, זכאית להאריך את חופשת הלידה ב-3 שבועות (מעבר ל-26 השבועות הקבועים בחוק) עבור כל תינוק נוסף ולקבל דמי לידה:
    *   יולדת הזכאית לדמי לידה לתקופה של 15 שבועות, תוכל להאריך את חופשת הלידה ב-3 שבועות עבור כל תינוק נוסף ולקבל דמי לידה עבור כל תקופה זו (מי שילדה תאומים זכאית לחופשת לידה ודמי לידה עבור 18 שבועות, מי שילדה שלישייה - עבור 21 שבועות וכו').
    *   יולדת הזכאית לדמי לידה לתקופה של 8 שבועות, תוכל להאריך את חופשת הלידה ב-3 שבועות עבור כל תינוק נוסף ולקבל דמי לידה עבור שבועיים מתוך 3 השבועות של תקופת הזכאות להארכה (מי שילדה תאומים זכאית לדמי לידה עבור 10 שבועות, מי שילדה שלישייה זכאית לדמי לידה עבור 12 שבועות וכו').

### אשפוז של היולדת או התינוק

*   יולדת שהיא, או התינוק שילדה, צריכים להישאר בבית החולים או לחזור לאשפוז בתוך חופשת הלידה הרגילה ל-15 ימים לפחות, זכאית להאריך את חופשת הלידה ולקבל דמי לידה נוספים עבור תקופת ההארכה. לפרטים נוספים ראו הארכת חופשת לידה בשל אשפוז של היולדת או של התינוק.
*   במקרים אלה ניתן גם לפצל את חופשת הלידה (להפסיק אותה זמנית למשך האשפוז, ולחדשה עם סיומו).

תהליך מימוש הזכות
-----------------

*   הזכות לחופשת לידה ניתנת באופן אוטומטי על ידי המעסיק.
*   המעסיק אינו רשאי למנוע מעובד/ת לצאת לחופשת לידה, והעובד/ת רשאי/ת לצאת לחופשת לידה ללא צורך בהסכמת המעסיק. אם המעסיק יפטר או יפגע בהיקף המשרה של העובד/ת, רשאי/ת העובד/ת להגיש נגדו תביעת פיצויים. למידע נוסף ראו:
    *   איסור פגיעה בהיקף משרה או בהכנסה של עובדת או עובד הנמצא/ת בחופשת לידה ולאחריה
    *   איסור פיטורי עובד/ת במהלך חופשת לידה
    *   איסור פיטורי עובד/ת לאחר חופשת לידה

*   מעסיק חייב להודיע לעובד או לעובדת על זכאותם להמשך הפרשות לביטוח פנסיוני או קרן השתלמות במהלך חופשת הלידה בהתאם להנחיות לפי טופס זה.
*   במקרה של עובדת - על המעסיק למסור את ההודעה תוך זמן סביר לאחר שנודע לו על ההיריון.
*   במקרה של עובד - על המעסיק למסור את ההודעה תוך זמן סביר מהיום שבו הודיע העובד על כוונתו לצאת לחופשת לידה.

צבירת זכויות סוציאליות במהלך חופשת הלידה
----------------------------------------

*   חופשת הלידה לא פוגעת בוותק של העובד/ת במקום העבודה.
*   במהלך חופשת הלידה ממשיך/ה העובד/ת לצבור זכויות סוציאליות המוקנות על פי הוותק במקום העבודה, כמו דמי הבראה, ימי מחלה ופיצויי פיטורים והעובד /ת ימשיכו לצבור זכויות אלה בזמן חופשת הלידה, כאילו הם המשיכו לעבוד בתקופה זו. צבירת הוותק לא נעצרת בגלל היציאה לחופשת לידה, והקשר המשפטי בין העובד/ת למעסיק אינו נפסק (ניתן למצוא התייחסות לכך בחוקים וצווי ההרחבה הרלוונטיים לזכויות הספציפיות).
*   לגבי חופשה שנתית - צבירת הוותק אומנם לא נעצרת בגלל היציאה לחופשת לידה אך יחד עם זאת, מספר ימי החופשה השנתית שהעובד/ת זכאי/ת להם במהלך השנה שבה יצא/ה לחופשת הלידה, ייקבעו לפי מספר ימי העבודה שעבד/ה בפועל באותה שנה יחסית ל-200. למידע על חישוב מספר ימי החופשה ראו חישוב מספר ימי החופשה השנתית.

*   עובדת העובדת במשרה מלאה 5 ימים בשבוע, החלה לעבוד ב-01.01.2015.
*   בשנת 2017 יצאה העובדת לחופשת לידה, ועבדה בפועל במהלך השנה 100 ימים בלבד.
*   מאחר וחופשת הלידה אינה מנתקת את הקשר המשפטי בין העובד והמעסיק, שנת 2017 תחשב כשנת עבודתה השלישית של העובדת .
*   עובד/ת שעבדו בשנת העבודה השלישית לפחות 200 ימים במשך השנה, זכאים ל-16 ימי חופשה ברוטו (12 ימי חופשה נטו ללא שישי ושבת).
*   היות שהעובד עבדה באותה שנה רק 100 ימים בפועל (בגלל חופשת הלידה), היא זכאית לחלק יחסי ממספר ימי הזכאות לחופשה ברוטו, בהתאם ליחס שבין ימי עבודתה בפועל ל-200.

    ![חישוב חופשה שנתית 200.jpg](/he/%D7%A7%D7%95%D7%91%D7%A5:%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%97%D7%95%D7%A4%D7%A9%D7%94_%D7%A9%D7%A0%D7%AA%D7%99%D7%AA_200.jpg)

*   העובדת זכאית ל-8 ימי חופשה ברוטו (6 ימים נטו) עבור שנת 2017 על פי החישוב הבא: 100 חלקי 200 כפול 16 (מספר הימים ברוטו) - סה"כ 8 ימים ברוטו (כולל שישי שבת), שהם 6 ימים חופשה נטו.

*   המעסיק חייב להמשיך להפריש את ההפרשות החודשיות לביטוח הפנסיוני של העובד/ת גם בעת חופשת הלידה אולם רק עבור החלק של החופשה שעבורו משולמים לעובד/ת דמי לידה. אם המעסיק נהג להפריש לקופת גמל נוספת או לקרן השתלמות, עליו להמשיך ולבצע את ההפרשות הללו גם בעת חופשת הלידה. לפרטים נוספים ראו **הפרשות לביטוח פנסיוני ולקרן השתלמות בחופשת לידה**.
*   על-פי הפסיקה, כאשר מעסיק מעניק לעובדיו שי לחג, עליו להעניק את השי גם לעובדים הנמצאים בחופשת לידה. לקריאת פסק דין בנושא זה ראו אין להפלות עובדת בחופשת לידה בהענקת שי לחג.

הטבות מס להורה לאחר לידה
------------------------

*   עובד או עובדת היוצאים לחופשת לידה עשויים להיות זכאים להטבות במס הכנסה, כבר בשנת המס שבה נולד התינוק.

*   עובד/ת שיצא/ה לחופשת לידה וקיבל/ה דמי לידה, עשוי להיות זכאי להחזר מס, מכיוון שמס ההכנסה שנוכה ממשכורתו לפני היציאה לחופשת הלידה, חושב על בסיס גובה השכר ולא על בסיס גובה דמי הלידה שהם נמוכים יותר. בנוסף בעת חישוב המס טרם הוענקו נקודות הזיכוי ממס הכנסה אשר מוענקים רק לאחר הלידה רטרואקטיבית לכל השנה.
*   לדוגמה מספרית ראו החזר מס הכנסה.
*   להסבר ספציפי על החזר מס לעובדת שחזרה מחופשת לידה ראו החזר מס הכנסה לאישה אחרי חופשת לידה.

*   בעקבות הלידה זכאים שני ההורים לנקודות זיכוי נוספות ממס הכנסה (רטרואקטיבית מתחילת השנה), גם אם לא יצאו לחופשת לידה.
    *   אם העובד/ת חזר/ה לעבודה מחופשת הלידה לפני שהסתיימה שנת המס (שבה נולד התינוק) עליו לעדכן את הפרטים בטופס 101 בהקדם ולפני שמסתיימת שנת המס. עדכון הפרטים לפני סוף השנה יאפשר למעסיק להעניק לעובד/ת את ההטבה דרך תלוש המשכורת רטרואקטיבית עבור כל השנה.
    *   אם העובד/ת חזר/ה לעבודה לאחר שהסתיימה שנת המס (כלומר חופשת הלידה החלה בשנה מסוימת אך העובד/ת חזר/ה לעבודה בשנה שלאחר מכן), יש להגיש בקשה להחזר מס על השנה שבה נולד הילד.

יולדת יצאה לחופשת לידה באוקטובר 2017 וחזרה לעבודה בינואר 2018.

*   העובדת זכאית לנקודות זיכוי בגין הלידה עבור כל שנת 2017.
*   מכיוון ששנת 2017 הסתיימה, לא ניתן לקבל את ההטבה דרך המשכורת ועל העובדת להגיש בקשה להחזר מס הכנסה עבור שנת 2017.
*   **שימו לב: מילוי טופס 101 בתחילת שנת 2018 אינו חל רטרואקטיבית ולא יאפשר לכם לקבל את הזיכוי עבור שנת 2017. אם לא קיבלתם את הזיכוי בשנת 2017 תוכלו להגיש בשנת 2018 בקשה להחזר מס לפקיד השומה.**

*   למידע על נקודות הזיכוי שמוענקות לעובדים שהפכו להורים ראו:
    *   נקודות זיכוי להורה לפעוט (מתחת לגיל 6) "נקודות זיכוי ממס הכנסה להורה לפעוט (מתחת לגיל 6)")
    *   נקודות זיכוי להורה לילד עד גיל 5 (הטבה זו ניתנת החל משנת המס שלאחר השנה שבה נולד התינוק)
    *   נקודות זיכוי להורה לילד עד גיל 18 (בלידה שהתרחשה ב-2017 או 2018 העובדת יכולה לדחות נקודת זיכוי אחת מהן לשנה שלאחר הלידה)
    *   למידע על נקודות זיכוי נוספות ראו פורטל נקודות זיכוי ממס הכנסה.

נסיעה לחו"ל במהלך חופשת הלידה
-----------------------------

*   נסיעה לחו"ל של יולדת שנמצאת בחופשת לידה לא פוגעת בזכאותה לדמי לידה.
*   אם בן הזוג של היולדת נוסע לחו"ל תיפסק חופשת הלידה (תקופת הורות ולידה) שמזכה אותו בדמי לידה לבן זוג של יולדת וזאת בשני המקרים:
    *   בחופשת לידה שלקח במקביל לחופשת הלידה של היולדת.
    *   בחופשה שבה הוא מחליף את היולדת והיא חוזרת לעבודה מוקדם יותר.
*   אם בן הזוג יצא לחו"ל לפני שהשלים 7 ימים רצופים של חופשת לידה תישלל ממנו הזכאות לדמי לידה גם עבור הימים שקדמו ליציאתו מהארץ.

כדאי לדעת
---------

*   **אסור לפטר עובדות ועובדים במהלך חופשת הלידה.**
*   חופשת הלידה נמשכת באופן רציף מלבד למקרים שבהם ניתן לפצל אותה עקב אשפוז היולדת או התינוק. ימי חג או ימי אבל לא עוצרים את חופשת הלידה ולא מזכים את היולדות או את בני זוגן באפשרות להאריך או לפצל את החופשה.
*   הורים שנמצאים בחופשת לידה עשויים להיות זכאים לסיוע במימון מסגרות לגיל הרך. למידע נוסף ראו סיוע להורים עובדים במימון מעונות יום ומשפחתונים - "הורים שנמצאים בחופשת לידה (תקופת לידה והורות)".

גורמים מסייעים
--------------

### מוקדים ממשלתיים

### ארגוני סיוע

*   לרשימת ארגוני סיוע בתחום התעסוקה, כולל הארגונים המסייעים ספציפית לנשים

### גורמי ממשל

*   לרשימת גורמי ממשל האחראיים על נושא התעסוקה, כולל הגופים העוסקים ספציפית בתחום תעסוקת נשים

מקורות משפטיים ורשמיים
----------------------

### פסקי דין

*   גמלה לשמירת היריון של עובדת שחזרה מחופשת לידה תחושב על בסיס השכר הרגיל שהיתה מרוויחה אלמלא החופשה
*   עובדת זכאית לפיצויים עבור עבודה בזמן חופשת לידה גם אם היא עבדה מרצונה

### חקיקה ונהלים

*   חוק עבודת נשים - סעיף 6.
*   חוק הביטוח הלאומי - סעיפים 56-48.
*   חוק שינויים בהסדרת תקופת הלידה וההורות (תיקוני חקיקה), התשע"ז -2017.
*   תקנות עבודת נשים (חופשת לידה חלקית לעובד שאשתו ילדה), התשנ"ט-1999.
*   תקנות עבודת נשים (הודעה על הסכמה לקיצור תקופת חופשת הלידה), התשע"ד-2014.
    """

    result = generate_response(question, user_profile, document)
    print("Generated Response:")
    print(result)