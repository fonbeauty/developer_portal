import allure


def allure_labels(feature: str, story: str, title: str):
    allure.dynamic.feature(feature)
    allure.dynamic.story(story)
    allure.dynamic.title(title)
