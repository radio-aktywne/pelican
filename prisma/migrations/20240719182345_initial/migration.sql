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

-- CreateTable
CREATE TABLE
  "bindings" (
    "id" UUID NOT NULL,
    "playlist_id" UUID NOT NULL,
    "media_id" UUID NOT NULL,
    "rank" STRING(16384) NOT NULL,
    CONSTRAINT "bindings_pkey" PRIMARY KEY ("id")
  );

-- CreateIndex
CREATE UNIQUE INDEX "name_unique" ON "media" ("name");

-- CreateIndex
CREATE UNIQUE INDEX "name_unique" ON "playlists" ("name");

-- CreateIndex
CREATE UNIQUE INDEX "playlist_id_rank_unique" ON "bindings" ("playlist_id", "rank");

-- AddForeignKey
ALTER TABLE "bindings"
ADD CONSTRAINT "playlist_id_fkey" FOREIGN KEY ("playlist_id") REFERENCES "playlists" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "bindings"
ADD CONSTRAINT "media_id_fkey" FOREIGN KEY ("media_id") REFERENCES "media" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
