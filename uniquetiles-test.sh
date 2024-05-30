clear
rm -f test-out/*.png
echo "xxx" > test-out/already-exists

echo "=== Converting 10 files, one verbosely ==="
python3 uniquetiles.py test-in/small-grayscale.png test-out/small-grayscale.png
python3 uniquetiles.py test-in/small-indexed.png   test-out/small-indexed.png
python3 uniquetiles.py test-in/small-rgb.png       test-out/small-rgb.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-default.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-a.png        --order a
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-ca.png       --order ca
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-p.png        --order p
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-default.png --verbose
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-10x5-a.png  --width 10 --height 5 --order a
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-a.png       --order a
echo

echo "=== These should cause three distinct errors before files are opened ==="
python3 uniquetiles.py test-in/wolf3d.png  test-out/test1.png --width 0
python3 uniquetiles.py test-in/nonexistent test-out/test2.png
python3 uniquetiles.py test-in/wolf3d.png  test-out/already-exists
echo

echo "=== These should cause four distinct errors after files are opened ==="
python3 uniquetiles.py test-in/wolf3d.png     test-out/nonexistent/
python3 uniquetiles.py test-in/small-rgba.png test-out/small-rgba.png
python3 uniquetiles.py test-in/wolf3d.png     test-out/test3.png --width 7
python3 uniquetiles.py test-in/wolf3d.png     test-out/test4.png --height 7
echo

echo "=== Validating output files (using a different PNG encoder may give false errors) ==="
md5sum -c --quiet uniquetiles-test.md5
echo

rm test-out/already-exists
