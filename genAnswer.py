import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# query = '[INST]<<SYS>>\nBạn là một trợ lý hữu dụng sử dụng tiếng Việt, biết tôn trọng và thành thật. Bạn luôn luôn trả lời các câu hỏi một cách có ích nhiều nhất có thể, nhưng đồng thời phải an toàn. Câu trả lời của bạn không được bao gồm các ngôn từ độc hại phân biệt chủng tộc, phân biệt giới tính, nguy hiểm, nội dung vi phạm pháp luật. Làm ơn hãy chắc chắn câu trả lời của bạn tự nhiên, tích cực và không thiên vị bất cứ cái gì. Nếu có câu hỏi không hợp lý hoặc không rõ ràng thì hãy giải thích tại sao thay vì trả lời không đúng sự thật. Nếu bạn không biết câu trả lời thì đừng chia sẻ thông tin sai sự thật. <</SYS>>\nNhiệm vụ của bạn là dựa vào đoạn văn nằm trong dấu triple back tick, hãy trả lời câu hỏi sau bằng tiếng Việt : {question}\nĐoạn văn : ```{context} ``` [/INST ]'

query = '''
Bạn là một mô hình phân tích và tạo đầu ra theo định dạng tôi quy ước.
Đầu vào: cấu trúc chứa thông tin câu hỏi.
Đầu ra: Trả về kết quả theo định dạng như ban đầu, thêm kết quả theo:
- Nếu yêu cầu dạng chọn đáp án đúng A, B, C, D thì ghi lại toàn bộ đáp án, đáp án đúng thì thêm zz vào trước. Ví dụ: zzA. ...
- Nếu yêu cầu dạng điền từ vào chỗ trống thì ghi đáp án vào 2 dấu ngoặc vuông [[]]. Ví dụ: Thân em vừa trắng lại vừa [[tròn]].
- Nếu yêu cầu đề là nối chéo cột bên trái, cột bên phải thì đưa về dạng điền khuyết, cột bên trái giữ nguyên, đáp án thêm vào bên phải. Ví dụ:
    - Giữa trưa, [[con kênh như một con suối lửa]].
    - Buổi sáng, [[con kênh như một dòng thủy ngân lóa mắt]].
    - Buổi chiều, [[con kênh phơn phớt màu đào]].
- Nếu yêu cầu đề là dạng sắp xếp theo từng từ thì đưa về dạng điền khuyết, đáp án được thêm vào các dấu [[]]. Ví dụ: [[Hôm nay]] [[tôi]] [[đi]] [[học]].
- Nếu yêu cầu đề là dạng sắp xếp theo từng chữ thì đưa về dạng kéo thả, đáp án được thêm vào các dấu [()]. Ví dụ: [(H)] [(ọ)] [(c)] [(t)] [(ậ)] [(p)]
- Dấu [...] thì để nguyên, không thay đổi.  
- Nội dung câu hỏi và đáp án không được thay đổi, chỉ thêm vào đáp án theo định dạng tôi quy ước.

Ví dụ:
Input:
Câu 1.
Điền từ còn thiếu để hoàn thành câu tục ngữ sau:
Chị ngã em [[]].

Output:
Câu 1.
Điền từ còn thiếu để hoàn thành câu tục ngữ sau:
Chị ngã em [[nâng]].

Input:
Câu 2.
Nối câu văn ở cột bên trái với nhóm thích hợp ở cột bên phải.
Em được đi Hà Nội thăm lăng Bác.
Hà Nội là Thủ đô của nước ta.
Nước Hồ Gươm xanh biếc quanh năm.


Cột bên phải
Câu nêu hoạt động
Cột bên phải
Câu nêu đặc điểm
Cột bên phải
Câu giới thiệu

Output:
Câu 2.
Nối câu văn ở cột bên trái với nhóm thích hợp ở cột bên phải.
Cột bên trái:
- Em được đi Hà Nội thăm lăng Bác. [(Câu nêu hoạt động)]
- Hà Nội là Thủ đô của nước ta. [(Câu giới thiệu)]
- Nước Hồ Gươm xanh biếc quanh năm. [(Câu nêu đặc điểm)]

Cột bên phải:
- Câu nêu hoạt động
- Câu nêu đặc điểm
- Câu giới thiệu

Input:
Câu 3.
Kéo các từ vào nhóm thích hợp
trường học
gần gũi
ân cần
ngôi nhà
chăm sóc
che chở
hiền từ
thư viện
bảo ban
Từ ngữ chỉ đặc điểm
Từ ngữ chỉ hoạt động
Từ chỉ sự vật

Output:
Câu 3.
Kéo các từ vào nhóm thích hợp:
- trường học
- gần gũi
- ân cần
- ngôi nhà
- chăm sóc
- che chở
- hiền từ
- thư viện
- bảo ban

Từ ngữ chỉ đặc điểm [[gần gũi || hiền từ || ân cần]], [[gần gũi || hiền từ || ân cần]], [[gần gũi || hiền từ || ân cần]]
Từ ngữ chỉ hoạt động [[chăm sóc || che chở || bảo ban]], [[chăm sóc || che chở || bảo ban]], [[chăm sóc || che chở || bảo ban]]
Từ chỉ sự vật [[trường học || ngôi nhà || thư viện]], [[trường học || ngôi nhà || thư viện]], [[trường học || ngôi nhà || thư viện]]

Input:
Câu 4.
Từ nào dưới đây có nghĩa giống với từ "hoạt bát"?
A.
nhiệt tình
B.
nồng nhiệt
C.
nhanh nhẹn
D.
nhanh chóng

Output:
Câu 4.
Từ nào dưới đây có nghĩa giống với từ "hoạt bát"?
A. nhiệt tình
B. nồng nhiệt
zzC. nhanh nhẹn
D. nhanh chóng

Input:
Câu 5.
Điền dấu câu thích hợp vào chỗ trống:
Ôi, buổi biểu diễn múa rối nước thật thú vị [[]]
Bạn có muốn đi xem múa rối nước với tớ không [[]]
Các nghệ nhân khéo léo điều khiển con rối trên mặt nước [[]]

Output:
Câu 5.
Điền dấu câu thích hợp vào chỗ trống:
Ôi, buổi biểu diễn múa rối nước thật thú vị [[!]]
Bạn có muốn đi xem múa rối nước với tớ không [[?]]
Các nghệ nhân khéo léo điều khiển con rối trên mặt nước [[.]]

Input:
Câu 6.
Sắp xếp các tiếng sau thành câu văn hoàn chỉnh.
mông.
có
em
cánh
Quê
đồng
mênh
hương

Output:
Câu 6.
Sắp xếp các tiếng sau thành câu văn hoàn chỉnh.
- mông.
- có
- em
- cánh
- Quê
- đồng
- mênh
- hương

[(Quê)] [(hương)] [(em)] [(có)] [(cánh)] [(đồng)] [(mênh)] [(mông)]

Input:
Câu 7:
Kéo các câu vào nhóm thích hợp.
Cháu nhớ ông bà lắm ạ!
Lớp bạn có bao nhiêu thành viên?
Con mặc thêm áo ấm đi!
Con yêu bố mẹ rất nhiều!
Ông bà có khoẻ không ạ?
Em gấp quần áo giúp chị nhé!
Câu khiến
Câu cảm
Câu hỏi

Output:
Câu 7:
Kéo các câu vào nhóm thích hợp.
- Cháu nhớ ông bà lắm ạ!
- Lớp bạn có bao nhiêu thành viên?
- Con mặc thêm áo ấm đi!
- Con yêu bố mẹ rất nhiều!
- Ông bà có khoẻ không ạ?
- Em gấp quần áo giúp chị nhé!

Câu khiến [[Cháu nhớ ông bà lắm ạ! || Con mặc thêm áo ấm đi! ]], [[Cháu nhớ ông bà lắm ạ! || Con mặc thêm áo ấm đi! ]]
Câu cảm [[Con yêu bố mẹ rất nhiều! || Con nhớ ông bà lắm ạ! ]], [[Cháu nhớ ông bà lắm ạ! || Con mặc thêm áo ấm đi! ]]
Câu hỏi [[Lớp bạn có bao nhiêu thành viên? || Ông bà có khoẻ không ạ? ]], [[Cháu nhớ ông bà lắm ạ! || Con mặc thêm áo ấm đi! ]]

Input:
Câu 8.
Chọn tiếng thích hợp điền vào chỗ trống sau:
Tiếng "chất" có thể ghép với tiếng (Chọn một trong các đáp án:
phác
liệu
vấn
) để tạo thành tính từ.

Output:
Câu 8.
Chọn tiếng thích hợp điền vào chỗ trống sau:
Tiếng "chất" có thể ghép với tiếng [[liệu]] để tạo thành tính từ.

Hãy thực hiện với: {html}
'''
def generate_prompt_data(prompt):
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"Lỗi khi kiểm tra tìm kiếm với Gemini: {e}")
        return False

def duyet_thu_muc(duong_dan):
    for thu_muc_goc, thu_muc_con, tap_tin in os.walk(duong_dan):
        # print(thu_muc_goc)
        if tap_tin:
            index = 0
            for ten_tap_tin in tap_tin:
                if ten_tap_tin.endswith('.txt'):
                    print(index)
                    duong_dan_tep_tin = os.path.join(thu_muc_goc, ten_tap_tin)

                    with open(duong_dan_tep_tin, 'r', encoding='utf-8') as file:
                        noi_dung = file.read()

                    duong_dan_tep_tin_moi = duong_dan_tep_tin.replace('.txt', ' - answer.txt')
                    query_gemini = query.replace("{html}", noi_dung)
                    gen_answer = generate_prompt_data(query_gemini)

                    with open(duong_dan_tep_tin_moi, 'w', encoding='utf-8') as new_file:
                        new_file.write(gen_answer)

                    time.sleep(12)
                    index += 1

def main_gen_answer(path_folder):
    print('Tạo câu trả lời')
    duyet_thu_muc(path_folder)