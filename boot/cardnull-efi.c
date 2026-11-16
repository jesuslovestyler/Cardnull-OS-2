// Cardnull's own EFI doorman — the UEFI boot loader of
// Cardnull OS 2 (Stone 16). Public domain, like
// everything in Cardnull.
//
// This is the disc's EFI door: a small EFI application
// standing at \EFI\BOOT\BOOTX64.EFI on the disc's EFI
// system partition, where the firmware looks for it. It
// does at this door what Cardnull's own BIOS doorman
// (boot/cardnull-boot.asm, Stone 11) does at its door,
// and nothing more:
//
//   1. It reads the system and its modules from the
//      partition it stands on — \boot\cardnull.elf,
//      \boot\settings.bin, \boot\feather.fea, and
//      \boot\paint.fea (Stone 24: the second feather,
//      its own module with its own card, received
//      through the same door as the first), and
//      \boot\calc.fea (Stone 30: the third feather, its
//      own module with its own card, received through
//      the same door as its sisters)
//      — the copies the disc lays there for this door.
//   2. When the system's own header asks for a picture
//      screen (the multiboot video request, Stone 9), it
//      asks the firmware's graphics for that very shape
//      and keeps the grant — address, pitch, size, and
//      the color fields' places — for the information.
//   3. It lays the multiboot information down in low
//      memory, in the BIOS doorman's own shape: the
//      information at 0x4000, the module table at
//      0x4400, the memory map at 0x4800 (the firmware's
//      map, turned into the multiboot reckoning), and
//      the modules in a row at 0x300000.
//   4. It lays the system's ELF segments where they
//      belong, leaves the firmware's services behind
//      (ExitBootServices), and hands over through the
//      handover piece (cardnull-efi-hand.S) copied onto
//      a low page of its own claiming — the step down
//      out of the firmware's 64-bit world into 32-bit
//      protected mode with paging off — ending with the
//      multiboot mark in EAX, the information's address
//      in EBX, interrupts off: the very handover the
//      BIOS door makes. (The handover runs from low
//      ground of the doorman's own choosing since the
//      witness fix: a firmware may lay this doorman's
//      image above the four-billion line, and the step
//      down cannot be walked from up there — see the
//      handover's own header.)
//
// It borrows nothing at the door: no GRUB stands here
// any more, at either door. If anything it needs is not
// found — a file, the system's shape, the picture it
// asks for, the low pages the information and the
// system must stand on — it says so on the screen in
// plain words and stops, rather than handing over a
// machine half-laid.
//
// The loader is freestanding C, compiled for the
// firmware's own calling way (the Windows x64 ABI the
// UEFI world speaks) and linked as a PE application of
// the EFI kind; build-iso.sh tells the whole building
// of it. The protocol shapes below are the UEFI
// specification's own, written out by hand — no library
// stands between this file and the firmware.

typedef unsigned long long u64;
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef void *efi_handle;
typedef u64 efi_status;

#define EFI_OK 0

// ---- the small tools the loader keeps for itself ----

static void byteset(void *dst, u8 v, u64 n) {
    u8 *d = (u8 *)dst;
    for (u64 i = 0; i < n; i++) d[i] = v;
}

static void bytecopy(void *dst, const void *src, u64 n) {
    u8 *d = (u8 *)dst;
    const u8 *s = (const u8 *)src;
    for (u64 i = 0; i < n; i++) d[i] = s[i];
}

// The compiler may ask for these by name; they are the
// two above, under their library names.
void *memset(void *dst, int v, unsigned long n) {
    byteset(dst, (u8)v, n);
    return dst;
}

void *memcpy(void *dst, const void *src, unsigned long n) {
    bytecopy(dst, src, n);
    return dst;
}

// ---- the firmware's shapes (UEFI specification) ----

typedef struct {
    u64 signature;
    u32 revision;
    u32 header_size;
    u32 crc32;
    u32 reserved;
} efi_table_header;

typedef struct {
    void *reset;
    efi_status (*output_string)(void *self, u16 *text);
    void *rest[8];
} efi_text_output;

typedef struct {
    efi_table_header header;
    void *raise_tpl;
    void *restore_tpl;
    efi_status (*allocate_pages)(u32 type, u32 mem_type, u64 pages, u64 *memory);
    efi_status (*free_pages)(u64 memory, u64 pages);
    efi_status (*get_memory_map)(u64 *size, void *map, u64 *key, u64 *desc_size, u32 *desc_version);
    efi_status (*allocate_pool)(u32 mem_type, u64 size, void **buffer);
    efi_status (*free_pool)(void *buffer);
    void *create_event;
    void *set_timer;
    void *wait_for_event;
    void *signal_event;
    void *close_event;
    void *check_event;
    void *install_protocol_interface;
    void *reinstall_protocol_interface;
    void *uninstall_protocol_interface;
    efi_status (*handle_protocol)(efi_handle handle, const void *guid, void **interface);
    void *reserved;
    void *register_protocol_notify;
    void *locate_handle;
    void *locate_device_path;
    void *install_configuration_table;
    void *load_image;
    void *start_image;
    void *exit;
    void *unload_image;
    efi_status (*exit_boot_services)(efi_handle handle, u64 key);
    void *get_next_monotonic_count;
    efi_status (*stall)(u64 microseconds);
    efi_status (*set_watchdog_timer)(u64 timeout, u64 code, u64 data_size, void *data);
    void *connect_controller;
    void *disconnect_controller;
    void *open_protocol;
    void *close_protocol;
    void *open_protocol_information;
    void *protocols_per_handle;
    void *locate_handle_buffer;
    efi_status (*locate_protocol)(const void *guid, void *registration, void **interface);
} efi_boot_services;

typedef struct {
    efi_table_header header;
    u16 *firmware_vendor;
    u32 firmware_revision;
    u32 reserved2;
    efi_handle console_in_handle;
    void *con_in;
    efi_handle console_out_handle;
    efi_text_output *con_out;
    efi_handle standard_error_handle;
    efi_text_output *std_err;
    void *runtime_services;
    efi_boot_services *boot_services;
    u64 number_of_table_entries;
    void *configuration_table;
} efi_system_table;

typedef struct {
    u32 data1;
    u16 data2;
    u16 data3;
    u8 data4[8];
} efi_guid;

typedef struct {
    u32 revision;
    efi_handle parent_handle;
    efi_system_table *system_table;
    efi_handle device_handle;
    void *file_path;
    void *reserved;
    u32 load_options_size;
    void *load_options;
    void *image_base;
    u64 image_size;
    u32 image_code_type;
    u32 image_data_type;
    void *unload;
} efi_loaded_image;

typedef struct efi_file efi_file;
struct efi_file {
    u64 revision;
    efi_status (*open)(efi_file *self, efi_file **new_handle, u16 *name, u64 mode, u64 attributes);
    efi_status (*close)(efi_file *self);
    void *del;
    efi_status (*read)(efi_file *self, u64 *size, void *buffer);
    void *write;
    void *get_position;
    efi_status (*set_position)(efi_file *self, u64 position);
    efi_status (*get_info)(efi_file *self, const efi_guid *type, u64 *size, void *info);
    void *set_info;
    void *flush;
};

typedef struct {
    u64 revision;
    efi_status (*open_volume)(void *self, efi_file **root);
} efi_simple_fs;

// The graphics door: the firmware's own picture screen.
typedef struct {
    u32 version;
    u32 horizontal;
    u32 vertical;
    u32 pixel_format;
    u32 red_mask;
    u32 green_mask;
    u32 blue_mask;
    u32 reserved_mask;
    u32 pixels_per_scanline;
} efi_gop_info;

typedef struct {
    u32 max_mode;
    u32 mode;
    efi_gop_info *info;
    u64 size_of_info;
    u64 frame_buffer_base;
    u64 frame_buffer_size;
} efi_gop_mode;

typedef struct {
    efi_status (*query_mode)(void *self, u32 mode, u64 *size, efi_gop_info **info);
    efi_status (*set_mode)(void *self, u32 mode);
    void *blt;
    efi_gop_mode *mode;
} efi_gop;

typedef struct {
    u32 type;
    u32 reserved;
    u64 physical_start;
    u64 virtual_start;
    u64 number_of_pages;
    u64 attribute;
} efi_memory_descriptor;

static const efi_guid loaded_image_guid =
    { 0x5B1B31A1, 0x9562, 0x11d2, { 0x8E, 0x3F, 0x00, 0xA0, 0xC9, 0x69, 0x72, 0x3B } };
static const efi_guid simple_fs_guid =
    { 0x964E5B22, 0x6459, 0x11d2, { 0x8E, 0x39, 0x00, 0xA0, 0xC9, 0x69, 0x72, 0x3B } };
static const efi_guid gop_guid =
    { 0x9042A9DE, 0x23DC, 0x4A38, { 0x96, 0xFB, 0x7A, 0xDE, 0xD0, 0x80, 0x51, 0x6A } };
static const efi_guid file_info_guid =
    { 0x09576E92, 0x6D3F, 0x11D2, { 0x8E, 0x39, 0x00, 0xA0, 0xC9, 0x69, 0x72, 0x3B } };

// The firmware's memory kinds the multiboot map calls
// available (type 1): the free memory, and the kinds
// that become free when the boot services are left —
// the loader's own pages among them, and the system's,
// which this loader claims as its data. The rest keeps
// its honest multiboot kinds: the ACPI tables' ground
// is 3, and everything else is 2, not to be used.
static u32 mb_type_of(u32 efi_type) {
    switch (efi_type) {
    case 1:  // loader code
    case 2:  // loader data
    case 3:  // boot services code
    case 4:  // boot services data
    case 7:  // conventional memory
        return 1;
    case 9:  // ACPI reclaim memory
        return 3;
    default:
        return 2;
    }
}

// A mask's field: where it stands and how wide it is.
static u32 mask_pos(u32 mask) {
    u32 p = 0;
    while (mask != 0 && (mask & 1) == 0) { mask >>= 1; p++; }
    return p;
}

static u32 mask_size(u32 mask) {
    u32 s = 0;
    while ((mask & 1) == 1) { mask >>= 1; s++; }
    return s;
}

// The handover piece, in cardnull-efi-hand.S: a
// self-carrying span — code, gate table, and the
// gate's pointer — that this doorman copies onto a low
// page of its own claiming and calls there. It never
// returns.
extern char cardnull_tramp_start[];
extern char cardnull_tramp_end[];

// ---- the doorman's work ----

static efi_system_table *st;
static efi_boot_services *bs;

// The graphics door, once opened, and the picture that
// stood when the doorman arrived — kept here so a
// failure after the doorman sets its own picture can
// give the firmware its own picture back before the
// failure words are said (see stop).
static efi_gop *gop_saved;
static u32 gop_home_mode;
static int gop_mode_set;

// Says one plain line on the firmware's screen — the
// doorman's only words, and only on a failure road.
static void say(u16 *text) {
    if (st && st->con_out && st->con_out->output_string) {
        st->con_out->output_string(st->con_out, text);
        st->con_out->output_string(st->con_out, L"\r\n");
    }
}

static void stop(u16 *why) {
    // When the doorman has already set the picture the
    // system asked for, the firmware's text console
    // keeps drawing in the mode that stood when the
    // doorman arrived — words said now would land on a
    // screen nobody is shown. Give the firmware its own
    // picture back first, so the words stand on the
    // screen it draws. (Witness fix, November 15, 2026:
    // a failure at this door must be sayable on every
    // firmware, not only the ones whose console follows
    // a stranger's mode set.)
    if (gop_mode_set && gop_saved) {
        gop_saved->set_mode(gop_saved, gop_home_mode);
        gop_mode_set = 0;
    }
    say(L"Cardnull could not start:");
    say(why);
    for (;;) {
        __asm__ volatile ("hlt");
    }
}

// Reads one whole file from the volume's root into a
// fresh pool buffer; gives back the buffer and its
// length, or stops the machine in plain words.
static void read_file(efi_file *root, u16 *name, u8 **out, u64 *out_len) {
    efi_file *f = 0;
    if (root->open(root, &f, name, 1 /* read */, 0) != EFI_OK || f == 0) {
        stop(L"the disc does not carry the system whole.");
    }
    u8 info_buf[128];
    u64 info_size = sizeof(info_buf);
    if (f->get_info(f, &file_info_guid, &info_size, info_buf) != EFI_OK) {
        stop(L"the disc could not be read as its own.");
    }
    u64 len = *(u64 *)(info_buf + 8);  // FileSize
    if (len == 0 || len > (64ull << 20)) {
        stop(L"the disc does not carry the system whole.");
    }
    u8 *buf = 0;
    if (bs->allocate_pool(2 /* loader data */, len, (void **)&buf) != EFI_OK || buf == 0) {
        stop(L"this machine's memory would not hold the system.");
    }
    u64 got = len;
    if (f->read(f, &got, buf) != EFI_OK || got != len) {
        stop(L"the disc could not be read as its own.");
    }
    f->close(f);
    *out = buf;
    *out_len = len;
}

// Claims the pages at a given address for the system's
// use; a claim refused stops the machine, in plain
// words — a half-laid machine is never handed over.
// Claims the pages at a given address for the system's
// use, of the firmware memory kind named; a claim
// refused stops the machine, in plain words — a
// half-laid machine is never handed over.
static void claim_as(u64 address, u64 pages, u32 mem_type) {
    u64 at = address;
    if (bs->allocate_pages(2 /* at address */, mem_type, pages, &at) != EFI_OK) {
        stop(L"this machine's low memory is not free for the system.");
    }
}

static void claim(u64 address, u64 pages) {
    claim_as(address, pages, 2 /* loader data */);
}

efi_status efi_main(efi_handle image, efi_system_table *table) {
    st = table;
    bs = table->boot_services;
    bs->set_watchdog_timer(0, 0, 0, 0);

    // The volume this doorman stands on: the loaded
    // image's own device carries the partition, and the
    // system and its modules stand on it under \boot.
    efi_loaded_image *loaded = 0;
    if (bs->handle_protocol(image, &loaded_image_guid, (void **)&loaded) != EFI_OK || loaded == 0) {
        stop(L"the firmware would not say where this door stands.");
    }
    efi_simple_fs *fs = 0;
    if (bs->handle_protocol(loaded->device_handle, &simple_fs_guid, (void **)&fs) != EFI_OK || fs == 0) {
        stop(L"the disc could not be read as its own.");
    }
    efi_file *root = 0;
    if (fs->open_volume(fs, &root) != EFI_OK || root == 0) {
        stop(L"the disc could not be read as its own.");
    }

    u8 *kernel = 0, *settings = 0, *feather = 0, *paint = 0, *calc = 0;
    u64 kernel_len = 0, settings_len = 0, feather_len = 0, paint_len = 0, calc_len = 0;
    read_file(root, L"\\boot\\cardnull.elf", &kernel, &kernel_len);
    read_file(root, L"\\boot\\settings.bin", &settings, &settings_len);
    read_file(root, L"\\boot\\feather.fea", &feather, &feather_len);
    read_file(root, L"\\boot\\paint.fea", &paint, &paint_len);
    read_file(root, L"\\boot\\calc.fea", &calc, &calc_len);
    root->close(root);

    // The system's own asking, from its multiboot header
    // in the file's first 8192 bytes: the mark, its
    // flags, and — when the video flag stands — the
    // picture's shape at +32/+36/+40/+44 from the mark.
    u32 *kh = (u32 *)kernel;
    u64 words = kernel_len / 4;
    if (words > 2048) words = 2048;
    u64 mark = 0;
    int found = 0;
    for (u64 i = 0; i < words; i++) {
        if (kh[i] == 0x1BADB002) { mark = i; found = 1; break; }
    }
    if (!found) {
        stop(L"the system on this disc is not shaped as its own.");
    }
    u32 mb_flags_word = kh[mark + 1];
    int want_video = (mb_flags_word & 4) != 0;
    u32 ask_w = kh[mark + 9];   // +36
    u32 ask_h = kh[mark + 10];  // +40
    u32 ask_d = kh[mark + 11];  // +44

    // The picture, when one is asked: the firmware's
    // graphics are asked for that very shape, thirty-two
    // bits a pixel, and the grant is kept.
    u64 fb_addr = 0;
    u32 fb_pitch = 0, fb_width = 0, fb_height = 0;
    u8 fb_rpos = 0, fb_rsize = 0, fb_gpos = 0, fb_gsize = 0, fb_bpos = 0, fb_bsize = 0;
    int video_ok = 0;
    if (want_video) {
        efi_gop *gop = 0;
        if (bs->locate_protocol(&gop_guid, 0, (void **)&gop) != EFI_OK || gop == 0) {
            stop(L"this machine offers no picture screen.");
        }
        gop_saved = gop;
        gop_home_mode = gop->mode->mode;
        int chosen = -1;
        efi_gop_info *chosen_info = 0;
        // The mode numbers run from 0 to the firmware's
        // MaxMode — which is the LAST mode's own number,
        // not the count of modes. The search once stopped
        // one short of it, and on a firmware whose only
        // matching picture stands last in its list, the
        // door would have refused a picture that was
        // there to grant. (Witness fix.)
        for (u32 m = 0; m <= gop->mode->max_mode && m < 1024; m++) {
            u64 sz = 0;
            efi_gop_info *info = 0;
            if (gop->query_mode(gop, m, &sz, &info) != EFI_OK || info == 0) continue;
            if (info->horizontal == ask_w && info->vertical == ask_h) {
                if (info->pixel_format == 0 || info->pixel_format == 1 || info->pixel_format == 2) {
                    chosen = (int)m;
                    chosen_info = info;
                    break;
                }
            }
        }
        if (chosen < 0 || ask_d != 32) {
            stop(L"this machine offers no picture of the shape the system asks for.");
        }
        if (gop->set_mode(gop, (u32)chosen) != EFI_OK) {
            stop(L"this machine's picture screen would not be set.");
        }
        gop_mode_set = 1;
        efi_gop_mode *gm = gop->mode;
        efi_gop_info *info = gm->info;
        fb_addr = gm->frame_buffer_base;
        fb_pitch = info->pixels_per_scanline * 4;
        fb_width = info->horizontal;
        fb_height = info->vertical;
        if (info->pixel_format == 1) {          // blue, green, red in memory
            fb_rpos = 16; fb_gpos = 8; fb_bpos = 0;
            fb_rsize = 8; fb_gsize = 8; fb_bsize = 8;
        } else if (info->pixel_format == 0) {   // red, green, blue in memory
            fb_rpos = 0; fb_gpos = 8; fb_bpos = 16;
            fb_rsize = 8; fb_gsize = 8; fb_bsize = 8;
        } else {                                 // the masks say it
            fb_rpos = (u8)mask_pos(info->red_mask);
            fb_rsize = (u8)mask_size(info->red_mask);
            fb_gpos = (u8)mask_pos(info->green_mask);
            fb_gsize = (u8)mask_size(info->green_mask);
            fb_bpos = (u8)mask_pos(info->blue_mask);
            fb_bsize = (u8)mask_size(info->blue_mask);
        }
        video_ok = 1;
    }

    // The low ground the handover stands on: the
    // information and its tables (0x4000, six pages —
    // room for a long memory map), the handover's stack
    // page, and the modules' row at 0x300000.
    claim(0x4000, 6);
    claim(0x8F000, 1);
    u64 mods_total = settings_len + feather_len + paint_len + calc_len;
    claim(0x300000, (mods_total + 4095) / 4096);

    // The handover's own low page (witness fix): the
    // step down out of the firmware's world is walked
    // from a copy of the handover piece standing here,
    // at an address of the doorman's own choosing,
    // claimed as loader code so the firmware lets it be
    // run — never from wherever the firmware happened
    // to lay this doorman's image, which may stand
    // above the four-billion line, where the step
    // down's own addresses would be cut in half and the
    // machine lost before the system is ever reached.
    claim_as(0x8E000, 1, 1 /* loader code */);
    u64 tramp_len = (u64)(cardnull_tramp_end - cardnull_tramp_start);
    if (tramp_len == 0 || tramp_len > 4096) {
        stop(L"the system's door is not shaped as its own.");
    }
    bytecopy((void *)0x8E000, cardnull_tramp_start, tramp_len);

    // The system's segments, claimed and laid: program
    // headers at +28 in its ELF header, of the size at
    // +42, as many as the count at +44; each PT_LOAD's
    // bytes copied from the file to its own address, and
    // the rest of its memory wiped, as the BIOS doorman
    // lays them.
    u32 entry = *(u32 *)(kernel + 24);
    u32 phoff = *(u32 *)(kernel + 28);
    u32 phentsize = *(u16 *)(kernel + 42);
    u32 phnum = *(u16 *)(kernel + 44);
    for (u32 i = 0; i < phnum; i++) {
        u8 *ph = kernel + phoff + i * phentsize;
        u32 ptype = *(u32 *)(ph + 0);
        if (ptype != 1) continue;
        u32 poff = *(u32 *)(ph + 4);
        u32 paddr = *(u32 *)(ph + 12);
        u32 filesz = *(u32 *)(ph + 16);
        u32 memsz = *(u32 *)(ph + 20);
        u64 first = paddr & ~4095ull;
        u64 last = (paddr + memsz + 4095) & ~4095ull;
        if (last > first) claim(first, (last - first) / 4096);
        bytecopy((void *)(u64)paddr, kernel + poff, filesz);
        if (memsz > filesz) byteset((void *)(u64)(paddr + filesz), 0, memsz - filesz);
    }

    // The modules, in a row at 0x300000 — settings,
    // feather, paint feather, calculator feather, as at
    // the BIOS door. (Each feather carries its card at
    // its own head — Nifla Stone 20 — so no card module
    // rides anymore.)
    bytecopy((void *)0x300000, settings, settings_len);
    bytecopy((void *)(0x300000 + settings_len), feather, feather_len);
    bytecopy((void *)(0x300000 + settings_len + feather_len), paint, paint_len);
    bytecopy((void *)(0x300000 + settings_len + feather_len + paint_len), calc, calc_len);

    // The multiboot information, in the BIOS doorman's
    // shape. What does not depend on the firmware's final
    // memory map is laid now; the map itself, and the
    // memory figure it reckons, are laid in the leaving
    // loop below, from the map as it stands at the door.
    u32 *info = (u32 *)0x4000;
    byteset((void *)0x4000, 0, 0x6000);
    info[5] = 4;                    // mods_count (+20)
    info[6] = 0x4400;               // mods_addr (+24)
    info[12] = 0x4800;              // mmap_addr (+48)
    u32 *mods = (u32 *)0x4400;
    u32 at = 0x300000;
    mods[0] = at; at += (u32)settings_len; mods[1] = at; mods[2] = 0; mods[3] = 0;
    mods[4] = at; at += (u32)feather_len;  mods[5] = at; mods[6] = 0; mods[7] = 0;
    mods[8] = at; at += (u32)paint_len;    mods[9] = at; mods[10] = 0; mods[11] = 0;
    mods[12] = at; at += (u32)calc_len;    mods[13] = at; mods[14] = 0; mods[15] = 0;
    if (video_ok) {
        u64 *fbq = (u64 *)(0x4000 + 88);
        *fbq = fb_addr;
        info[24] = fb_pitch;        // +96
        info[25] = fb_width;        // +100
        info[26] = fb_height;       // +104
        u8 *fbb = (u8 *)(0x4000 + 108);
        fbb[0] = 32;                // bits a pixel
        fbb[1] = 1;                 // direct color
        fbb[4] = fb_rpos; fbb[5] = fb_rsize;
        fbb[6] = fb_gpos; fbb[7] = fb_gsize;
        fbb[8] = fb_bpos; fbb[9] = fb_bsize;
    }

    // The leaving: the firmware's map is taken and turned
    // into the multiboot map, the memory figure reckoned
    // from it, and the boot services left behind — and
    // if the map moved under the taking (its key gone
    // stale), the taking is done again, as the firmware's
    // own road prescribes.
    u8 *mapbuf = 0;
    if (bs->allocate_pool(2, 256 * 1024, (void **)&mapbuf) != EFI_OK || mapbuf == 0) {
        stop(L"this machine's memory would not hold its own map.");
    }
    int left = 0;
    for (int attempt = 0; attempt < 8 && !left; attempt++) {
        u64 map_size = 256 * 1024;
        u64 map_key = 0, desc_size = 0;
        u32 desc_version = 0;
        if (bs->get_memory_map(&map_size, mapbuf, &map_key, &desc_size, &desc_version) != EFI_OK) {
            stop(L"the firmware would not tell its memory.");
        }
        u8 *mmap = (u8 *)0x4800;
        u64 mmap_bytes = 0;
        u64 upper_kb = 0;
        u64 count = map_size / desc_size;
        for (u64 i = 0; i < count; i++) {
            efi_memory_descriptor *d = (efi_memory_descriptor *)(mapbuf + i * desc_size);
            u64 base = d->physical_start;
            u64 len = d->number_of_pages * 4096;
            if (len == 0) continue;
            u32 type = mb_type_of(d->type);
            if (mmap_bytes + 24 <= 0x5800) {
                u32 *e = (u32 *)(mmap + mmap_bytes);
                e[0] = 20;
                *(u64 *)(mmap + mmap_bytes + 4) = base;
                *(u64 *)(mmap + mmap_bytes + 12) = len;
                e[5] = type;
                mmap_bytes += 24;
            }
            if (type == 1 && base >= 1048576) {
                upper_kb += len / 1024;
            }
        }
        u32 flags = 73;             // memory + modules + map
        if (video_ok) flags |= 4096;
        info[0] = flags;
        info[1] = 640;              // mem_lower (+4)
        info[2] = (u32)upper_kb;    // mem_upper (+8)
        info[11] = (u32)mmap_bytes; // mmap_length (+44)
        if (bs->exit_boot_services(image, map_key) == EFI_OK) {
            left = 1;
        }
    }
    if (!left) {
        // The boot services were never left, so the
        // firmware's screen still answers: say so, and
        // stop. (Reaching here means eight takings of the
        // map each went stale at the door.) stop gives
        // the firmware its own picture back first, so
        // the words are seen.
        stop(L"the firmware would not let go of the machine.");
    }

    // The handover, called at its low copy: it never
    // returns.
    ((void (*)(u32, u32))(u64)0x8E000)(entry, 0x4000);
    return 0;  // never reached
}
