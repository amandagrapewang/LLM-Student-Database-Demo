from openai import OpenAI
import random
import os

# 配置OpenAI
api_key = "YOUR_API_KEY"
base_url = "YOUR_URL"
client = OpenAI(api_key=api_key, base_url=base_url)


# 定义一个虚拟数据库
students_database = {
    "2024101": {"name": "张三"},
    "2024102": {"name": "李四"},
    "2024103": {"name": "王五"},
}


# 添加学生信息
def add_student(student_id, name):
    if student_id in students_database:
        return False, "学生信息已存在。"
    students_database[student_id] = {"name": name}
    return True, "学生信息添加成功。"


def generate_random_student_name():
    prompt = "生成一个合适且格式正确的中文名字，字数范围在两个字到四个字之间，返回一个中文姓名就好"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # 检查response是否有choices属性
        if response.choices:
            # 直接获取第一个选择的message的content属性（返回response看了）
            name = response.choices[0].message.content.strip()
            # 检查生成的姓名是否为空
            if name:
                return name
            else:
                print("错误：生成的姓名为空。")
        else:
            print("错误：API响应中没有找到 'choices' 属性或它为空。")

    except Exception as e:
        print(f"生成学生姓名时发生未预料的错误：{e}")
    return "无名氏"


# 生成学生学号
def generate_random_student_id():
    return str("2024" + str(random.randint(100, 125)))


# 验证学生信息格式的函数
def validate_information_format(student_id, name):
    prompt = f"""
            请验证以下学生信息格式是否正确：学号 {student_id}，姓名 {name}, 
            其中学号应为2024开头的7位数字，
            姓名应是一个合适且格式正确的中文名字，只有一个中文姓名，
            如果这些要求均满足请回答中包含格式正确
            """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    if response and response.choices:
        print(response.choices[0].message.content)
        return "格式正确" in response.choices[0].message.content
    else:
        print("API 响应中没有找到有效的 choices 或者 message 属性不是预期的字符串。")
        return False


# 测试生成用例
def test_student_management_system_with_openai(num_tests=10):
    results = []
    for _ in range(num_tests):
        student_id = generate_random_student_id()
        name = generate_random_student_name()
        print(f"\n测试 {+_ + 1}: 学号 {student_id}，姓名 {name}")
        # 验证信息格式
        if not validate_information_format(student_id, name):
            results.append((student_id, name, "格式验证失败"))
            continue
        # 测试添加学生信息
        success, message = add_student(student_id, name)
        results.append((student_id, name, message))
    return results


# 主函数
def main():
    print("欢迎使用学生信息管理系统 - 自动测试模式")
    test_results = test_student_management_system_with_openai(20)
    for result in test_results:
        print(f"学号: {result[0]}, 姓名: {result[1]}, 结果: {result[2]}")
    # 写入文档存储测试数据
    file_path = os.path.join(os.getcwd(), 'else/test_results.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in test_results:
            file.write(f"学号: {result[0]}, 姓名: {result[1]}, 结果: {result[2]}\n")
    print(f"测试结果已保存到 '{file_path}' 文件。")


if __name__ == "__main__":
    main()