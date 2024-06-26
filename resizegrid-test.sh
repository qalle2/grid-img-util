clear
rm -f test-out/*.png
echo "xxx" > test-out/already-exists

echo "=== Converting ==="
python3 resizegrid.py test-in/8x8-pal.png test-out/8x8-pal.png
python3 resizegrid.py test-in/8x8-rgb.png test-out/8x8-rgb.png
python3 resizegrid.py test-in/8x8-rgb.png test-out/8x8-rgb-5x7.png --ow 5 --oh 7
python3 resizegrid.py test-in/8x8-rgb.png test-out/8x8-rgb-11x13-green.png --ow 11 --oh 13 --bgcolor 00ff00
echo

echo "=== These should cause four distinct errors before files are opened ==="
python3 resizegrid.py test-in/8x8-pal.png test-out/error3.png --ow 8 --oh 8
python3 resizegrid.py test-in/8x8-pal.png test-out/error4.png --bgcolor x
python3 resizegrid.py test-in/nonexistent test-out/error5.png
python3 resizegrid.py test-in/8x8-pal.png test-out/already-exists
echo

echo "=== These should cause three distinct errors after files are opened ==="
python3 resizegrid.py test-out/already-exists test-out/error6.png
python3 resizegrid.py test-in/8x8-rgba.png    test-out/error7.png
python3 resizegrid.py test-in/8x8-pal.png     test-out/nonexistent/
echo

echo "=== Validating output files (using a different PNG encoder may give false errors) ==="
md5sum -c --quiet resizegrid-test.md5
echo

rm test-out/error*.png
rm test-out/already-exists
