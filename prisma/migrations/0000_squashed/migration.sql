-- CreateTable
CREATE TABLE "media" (
  "id" UUID NOT NULL,
  "name" TEXT NOT NULL,
  CONSTRAINT "media_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "playlists" (
  "id" UUID NOT NULL,
  "name" TEXT NOT NULL,
  CONSTRAINT "playlists_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "bindings" (
  "id" UUID NOT NULL,
  "playlist_id" UUID NOT NULL,
  "media_id" UUID NOT NULL,
  "rank" TEXT NOT NULL,
  CONSTRAINT "bindings_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "media_name_unique" ON "media" ("name");

-- CreateIndex
CREATE UNIQUE INDEX "playlists_name_unique" ON "playlists" ("name");

-- CreateIndex
CREATE UNIQUE INDEX "bindings_playlist_id_rank_unique" ON "bindings" ("playlist_id", "rank");

-- AddForeignKey
ALTER TABLE "bindings"
ADD CONSTRAINT "bindings_playlist_id_fkey" FOREIGN KEY ("playlist_id") REFERENCES "playlists" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "bindings"
ADD CONSTRAINT "bindings_media_id_fkey" FOREIGN KEY ("media_id") REFERENCES "media" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
