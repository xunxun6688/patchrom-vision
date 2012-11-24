import common
import edify_generator

def DeleteFormat(info):
    edify = info.script
    for i in xrange(len(edify.script)):
        if "format" in edify.script[i] and "/dev/block/mmcblk0p25" in edify.script[i]:
            edify.script[i]="""format("ext4", "EMMC", "/dev/block/mmcblk0p25", "0");"""
        elif "mount" in edify.script[i] and "/dev/block/mmcblk0p25" in edify.script[i]:
            edify.script[i]="""mount("ext4", "EMMC", "/dev/block/mmcblk0p25", "/system");
delete_recursive("/system/lost+found", "/system/lib", "/system/app", "/system/bin", "/system/customize", "/system/etc", "/system/fonts", "/system/framework", "/system/media", "/system/tts", "/system/usr", "/system/xbin","/system/build.prop", "0");
run_program("/sbin/busybox", "rm", "/system/lib/*", "-rf");"""
    return

def AddAssertions(info): 
    edify = info.script
    for i in xrange(len(edify.script)):
	    if """set_perm_recursive(0, 2000, 0777, 0755, "/system/xbin");""" in edify.script[i]:
		    edify.script[i] = """set_perm_recursive(0, 2000, 0777, 0755, "/system/xbin");
set_perm_recursive(0, 2000, 0755, 0750, "/system/etc/init.d");
set_perm(0, 0, 0755, "/system/etc/init.d");
set_perm_recursive(0, 2000, 0755, 0750, "/system/etc/pre-init.d");
set_perm(0, 0, 0755, "/system/etc/pre-init.d");"""
    return

def FullOTA_InstallEnd(info):
    DeleteFormat(info)
    AddAssertions(info)

def AddIncrementalLibrary(info):
    info.output_zip.writestr("lib/libshell_jni.so", info.target_zip.read("SYSTEM/lib/libshell_jni.so"))
    info.output_zip.writestr("lib/libshellservice.so", info.target_zip.read("SYSTEM/lib/libshellservice.so"))
    info.output_zip.writestr("lib/libshell.so", info.target_zip.read("SYSTEM/lib/libshell.so"))
    info.output_zip.writestr("lib/libaudiofp.so", info.target_zip.read("SYSTEM/lib/libaudiofp.so"))
    info.output_zip.writestr("lib/libjni_resource_drm.so", info.target_zip.read("SYSTEM/lib/libjni_resource_drm.so"))
    info.output_zip.writestr("lib/libffmpeg_xm.so", info.target_zip.read("SYSTEM/lib/libffmpeg_xm.so"))
    info.output_zip.writestr("lib/liblocSDK_2.5OEM.so", info.target_zip.read("SYSTEM/lib/liblocSDK_2.5OEM.so"))
    info.output_zip.writestr("lib/libjni_latinime.so", info.target_zip.read("SYSTEM/lib/libjni_latinime.so"))
    info.script.AppendExtra('package_extract_dir("lib","/system/lib");');

def IncrementalOTA_InstallEnd(info):
    edify = info.script
    for i in xrange(len(edify.script)):
        if "mount" in edify.script[i] and "/dev/block/mmcblk0p25" in edify.script[i]:
            edify.script[i]="""mount("ext4", "EMMC", "/dev/block/mmcblk0p25", "/system");"""
    AddIncrementalLibrary(info)
    AddAssertions(info)
