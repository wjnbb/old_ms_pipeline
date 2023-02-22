singularity exec \
    -B /mnt/Volume1/data/mass-spec/msconvert/inputs:/data/inputs \
    -B /mnt/Volume1/data/mass-spec/runs/:/data/outputs \
    -B `mktemp -d /mnt/Volume1/tmp/wineXXX`:/mywineprefix \
    -w /mnt/Volume1/tools/pwiz_singularity/pwiz_sandbox \
    mywine msconvert \
        --mzXML \
    	--64 \
        --filter "peakPicking true 1-" \
        --ignoreUnknownInstrumentError \
        -o /data/outputs/20230210_GAI13P3_MSMS_2/mzxmls \
	--verbose \
        "/data/inputs/20230210_GAI13P3_MSMS/20230210_GAI13P3_MSMS.wiff2"
