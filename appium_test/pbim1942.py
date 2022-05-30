from time import sleep
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

SLEEP_TIME = 2

class NotepadAndroid(unittest.TestCase):
    @classmethod
    def setUp(self):
        desired_capabilities = {
            'platformName': 'Android',
            'platformVersion': '12',
            'udid': 'emulator-5554',
            'deviceName': 'Android Emulator',
            'app': '/media/pelokbal/MyPassport/Egyetem/Sem6/VeriVali/Cur/code/apks/notepad.apk'
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities)
        self.driver.implicitly_wait(30)

    @classmethod
    def tearDown(self):
        self.driver.quit()

    # UTILITY FUNCTIONS

    def findTitle(self):
        return self.driver.find_element("id",
            "com.atomczak.notepat:id/textNoteTitleEdit")

    def editTitle(self, title):
        self.findTitle().send_keys(title)

    def findText(self):
        return self.driver.find_element("id",
            "com.atomczak.notepat:id/textNoteContentEdit")

    def editText(self, text):
        self.findText().send_keys(text)

    def save(self):
        self.driver.find_element("id",
            "com.atomczak.notepat:id/action_save_note").click()

    def quit(self):
        self.driver.find_element("xpath",
            "//android.widget.ImageButton[@content-desc='Navigate up']").click()

    def saveAndQuit(self):
        self.save()
        self.quit()

    def findAllNotes(self):
        return self.driver.find_elements("id",
            "com.atomczak.notepat:id/note_list_title_text")

    def createNote(self, title, text=''):
        self.driver.find_element("xpath",
            "//android.widget.ImageButton[@content-desc='New note']").click()
        self.editTitle(title)
        self.editText(text)
        self.saveAndQuit()

    def searchNotes(self, searched):
        self.driver.find_element("id",
            "com.atomczak.notepat:id/action_search_note").click()
        self.driver.find_element("id",
            "com.atomczak.notepat:id/search_src_text").send_keys(searched)
        return self.findAllNotes()
        

    # TESTS
    def testNewNoteTitleShouldMatch(self):
        title = 'CustomTitle1'
        self.createNote(title)
        self.assertEqual(title, self.findAllNotes()[0].text)


    def testDeletedNoteShouldNotAppear(self):
        notes_count = len(self.findAllNotes())

        self.createNote('ToBeDeleted')
        self.findAllNotes()[0].click()
        self.driver.find_element("xpath",
            "//android.widget.ImageView[@content-desc='More options']").click()
        sleep(SLEEP_TIME)
        self.driver.find_elements_by_android_uiautomator('text("Delete")')[0].click()
        self.driver.find_elements_by_android_uiautomator('text("DELETE")')[0].click()

        self.assertEqual(notes_count, len(self.findAllNotes()))


    def testEditedTextShouldChange(self):
        old_text = 'Initial text'
        self.createNote('ToBeEdited', old_text)
        self.findAllNotes()[0].click()
        
        new_text = 'New text'
        self.assertNotEqual(old_text, new_text)
        self.editText(new_text)
        self.saveAndQuit()

        self.findAllNotes()[0].click()
        self.assertEqual(new_text, self.findText().text)


    def testSearchedNoteShouldBeFound(self):
        title = 'Title to be searched'
        old_count = len(self.searchNotes(title))

        self.createNote(title)
        self.assertEqual(old_count + 1, len(self.searchNotes(title)))


    def testTappedNoteShouldOpen(self):
        note = self.findAllNotes()[0]
        note_title = note.text

        action = TouchAction(self.driver)
        action.tap(note).perform()
        sleep(SLEEP_TIME)

        self.assertEqual(note_title, self.findTitle().text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NotepadAndroid)
    unittest.TextTestRunner(verbosity=1).run(suite)