AC_INIT([art-uuid], [1.0])
AC_CONFIG_SRCDIR([artuuid.c])
AC_CONFIG_HEADERS([config.h])
AM_INIT_AUTOMAKE([foreign -Wall])
AC_PROG_CC
dnl макрос из autoconf-archive: защитные флаги, если их понимает компилятор
AX_CHECK_COMPILE_FLAG([-fstack-protector-strong],
    [CFLAGS="$CFLAGS -fstack-protector-strong"])
AX_CHECK_COMPILE_FLAG([-Wextra], [CFLAGS="$CFLAGS -Wextra"])
AC_CHECK_HEADERS([uuid/uuid.h], [], [AC_MSG_ERROR([uuid/uuid.h not found, install libuuid development files])])
AC_SEARCH_LIBS([uuid_generate_random], [uuid], [], [AC_MSG_ERROR([libuuid not found])])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
