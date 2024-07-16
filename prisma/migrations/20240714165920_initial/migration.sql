-- CreateTable
CREATE TABLE
  "media" (
    "id" UUID NOT NULL,
    "name" STRING(255) NOT NULL,
    CONSTRAINT "media_pkey" PRIMARY KEY ("id")
  );

-- CreateIndex
CREATE UNIQUE INDEX "name_unique" ON "media" ("name");
