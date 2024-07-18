-- CreateTable
CREATE TABLE
  "media" (
    "id" UUID NOT NULL,
    "name" STRING(255) NOT NULL,
    CONSTRAINT "media_pkey" PRIMARY KEY ("id")
  );

-- CreateTable
CREATE TABLE
  "playlists" (
    "id" UUID NOT NULL,
    "name" STRING(255) NOT NULL,
    CONSTRAINT "playlists_pkey" PRIMARY KEY ("id")
  );

-- CreateIndex
CREATE UNIQUE INDEX "name_unique" ON "media" ("name");

-- CreateIndex
CREATE UNIQUE INDEX "name_unique" ON "playlists" ("name");
