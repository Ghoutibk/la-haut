// Les élisions du français devant le nom d'une direction : « de l'ouest », mais « du sud ».

function startsWithVowel(word: string): boolean {
  return /^[aeiouy]/i.test(word);
}

export function fromThe(direction: string): string {
  return startsWithVowel(direction) ? `de l'${direction}` : `du ${direction}`;
}

export function towardThe(direction: string): string {
  return startsWithVowel(direction) ? `vers l'${direction}` : `vers le ${direction}`;
}

export function theDirection(direction: string): string {
  return startsWithVowel(direction) ? `l'${direction}` : `le ${direction}`;
}
