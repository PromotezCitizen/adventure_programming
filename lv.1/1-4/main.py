from pnm import PNM

pnm = PNM()
pnm.load()
# 구현된 메소드
# pnm.reverseColor()
# pnm.drawSquare()
# pnm.mirrorTD()
# pnm.mirrorLR()
# pnm.turnRight()
# pnm.turnLeft()
pnm.save()

# 기본 문제
#   PPM 파일을 읽어 영상을 반전한 후에 그 결과를 새로운 PPM 파일에 저장하시오. 

# 제한요소 및 요구사항
#   ▪기본 메뉴를 제공한다. - 완료
#   ▪상세한 입력과 출력 메시지를 제공한다. - 완료
#   ▪2개 이상의 소스파일과 1개 이상의 헤더파일을 사용한다. - 완료
#   ▪전역 변수를 사용할 수 없다. - 완료

# 확장 문제
#   ▪영상을 반전한 후 주어진 위치에 사각형을 출력하고 그 결과를 새로운 PPM 파일에 저장하시오. - 완료
#   ▪회색음영 영상을 저장하는 PGM 파일의 구조를 분석하여 파일 포맷에 따라
#       PPM 또는 PGM 파일을 처리할 수 있도록 하시오. - 완료

# 추가로 구현 완료
#   ▪이미지 회전(rotate90, rotate-90)
#   ▪이미지 대칭(상하대칭, 좌우대칭)
#   ▪파일의 Magic Number을 통해 PPM, PGM파일을 자동으로 구분

# 구현해볼 내용
#   ▪PPM to PGM / PGM to PPM(convertExt)