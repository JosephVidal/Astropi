NAME	=	astropi

all:
	cp src/astropi.py $(NAME)
	chmod +x $(NAME)

clean:
	rm -rf $(NAME)
	find . -type f -name '*.pyc' -delete

.PHONY: all clean
