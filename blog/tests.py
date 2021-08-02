from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.

class TestView(TestCase):
    # TestCase 내에서 기본적으로 설정되어야 하는 내용이 있다면 setUp() 함수에서 정의
    def setUp(self):
        self.client = Client()
    
    def test_post_list(self):

        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')

        '''
        Django 테스트에서 client는 테스트를 위한 가상의 사용자라고 생각하면 된다.
        self.client.get('/blog/')로 사용자가 웹 브라우저에 '127.0.0.1:8000/blog/'를 입력했다고 가정하고
        그 상황에서 열리는 웹 페이지 정보를 response에 저장한다.
        '''

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        '''
        서버에서 요청한 페이지를 찾을 수 없을 때, 404 오류를 돌려주고
        서버에서 요청한 페이지를 성공적으로 결과를 돌려줄 때, 200을 보내도록 약속되어 있다.

        페이지가 정상적으로 열렸다면 response 데이터의 status_code 값이 200으로 나온다.
        '''

        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')

        '''
        불러온 페이지의 내용은 HTML로 되어 있다. HTML 요소에 쉽게 접근하기 위해서
        먼저 Beautifulsoup으로 읽어들이고, html.parser 명령어로 html 파일을 
        파싱한 결과를 soup라는 변수에 담는다. 
        '''

        self.assertEqual(soup.title.text, 'Blog')

        '''
        title 태그에서 text 요소면 가져와서 그 텍스트가 'Blog'인지 확인한다.
        '''

        # 1.4 네비게이션 바가 존재한다.
        navbar = soup.nav

        '''
        soup.nav로 soup에 담긴 내용 중 nav 태그의 요소들만 가져와서 navbar에 저장한다.
        '''

        # 1.5 Blog, About Me라는 문구가 내비게이션 바에 존재한다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        '''
        navbar의 텍스트 중에서 Blog와 About me가 있는 지 확인한다.
        '''

        # 2.1 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)

        '''
        작성된 포스트가 0개인지 확인한다.
        테스트가 시작되면 테스트를 위한 새 데이터베이스를 임시로 만들어서 진행한다.
        단, setUp() 함수에서 설정한 요소는 포함시킨다. 
        하지만 현재 setUp() 함수는 테스트를 위해 생성된 데이터베이스에 어떤 정보도 미리 담아 놓으라는 말이 없다.
        따라서, 현제 테스트 데이터베이스에는 포스트 데이터가 하나도 없어야 함.
        '''

        # 2.2 메인 영역에 '아직 게시물이 없습니다.'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')

        '''
        id가 'main-area'인 div 요소를 찾아서 main_area에 저장한다.
        '''

        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        '''
        데이터베이스에 저장된 Post 레코드가 하나도 없기 때문에 
        메인 영역에 '아직 게시물이 없습니다'라는 문구가 나타나는지 점검한다.
        '''

        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title="첫 번째 포스트입니다.",
            content="Hello, World. We are the world.",
        )
        post_002 = Post.objects.create(
            title="두 번째 포스트입니다.",
            content="1등이 전부는 아니자나요",
        )

        '''
        Post 레코드가 데이터베이스에 존재하는 상황도 테스트하기 위해 포스트 2개를 만든다.
        '''

        self.assertEqual(Post.objects.count(), 2)

        '''
        매개변수에 Post 모델의 필드 값을 넣고, 테스트 데이터베이스에 포스트 2개가 잘 생성되었는지 확인한다.
        '''

        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        '''
        페이지를 새로고침하기 위해 1.1 ~ 1.3의 과정 반복하여
        페이지가 정상적으로 열렸다면, status_code의 값 200을 받습니다.
        '''

        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        '''
        새로 만든 두 포스트 레코드의 타이틀이 div 태그의 id가 'main_area'인 요소에 있는 지 확인한다.
        '''

        # 3.4 '아직 게시물이 없습니다.'라는 문구가 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        '''
        두 개의 포스트 레코드가 생성되었으므로, '아직 게시물이 없습니다.'라는 문구가
        메인 영역에 더 이상 나타나지 않아야 한다.
        '''