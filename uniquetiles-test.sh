clear
rm -f test-out/*.png
echo "xxx" > test-out/already-exists

echo "=== Creating 11 files, one verbosely ==="
python3 uniquetiles.py test-in/small-grayscale.png          --outfile test-out/small-grayscale.png
python3 uniquetiles.py test-in/small-indexed.png            --outfile test-out/small-indexed.png
python3 uniquetiles.py test-in/small-rgb.png                --outfile test-out/small-rgb.png
python3 uniquetiles.py test-in/keen4.png                    --outfile test-out/keen4-default.png
python3 uniquetiles.py test-in/keen4.png                    --outfile test-out/keen4-a.png        --order a
python3 uniquetiles.py test-in/keen4.png                    --outfile test-out/keen4-ca.png       --order ca
python3 uniquetiles.py test-in/keen4.png                    --outfile test-out/keen4-p.png        --order p
python3 uniquetiles.py test-in/wolf3d.png                   --outfile test-out/wolf3d-default.png --verbose
python3 uniquetiles.py test-in/wolf3d.png                   --outfile test-out/wolf3d-10x5-a.png  --width 10 --height 5 --order a
python3 uniquetiles.py test-in/wolf3d.png                   --outfile test-out/wolf3d-a.png       --order a
python3 uniquetiles.py test-in/keen4.png test-in/wolf3d.png --outfile test-out/keen4,wolf3d.png
echo

echo "=== These should cause four distinct errors before files are opened ==="
python3 uniquetiles.py test-in/wolf3d.png  --outfile test-out/test1.png --width 0
python3 uniquetiles.py test-in/nonexistent --outfile test-out/test2.png
python3 uniquetiles.py test-in/wolf3d.png  --outfile test-out/already-exists
python3 uniquetiles.py test-in/wolf3d.png
echo

echo "=== These should cause four distinct errors after files are opened ==="
python3 uniquetiles.py test-in/wolf3d.png     --outfile test-out/nonexistent/
python3 uniquetiles.py test-in/small-rgba.png --outfile test-out/small-rgba.png
python3 uniquetiles.py test-in/wolf3d.png     --outfile test-out/test3.png --width 7
python3 uniquetiles.py test-in/wolf3d.png     --outfile test-out/test4.png --height 7
echo

echo "=== Validating output files (using a different PNG encoder may give false errors) ==="
md5sum -c --quiet uniquetiles-test.md5
echo

rm test-out/already-exists
