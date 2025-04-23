#pragma once

#define STRINGIFY(X) #X
#define KEYVAL(X) " " #X "=" STRINGIFY(X)


char delim[] = ", ";
char * firsttok(char *args) {
  return strtok(args, delim);
}
char * nexttok(char *args) {
  return strtok(nullptr, delim);
}
